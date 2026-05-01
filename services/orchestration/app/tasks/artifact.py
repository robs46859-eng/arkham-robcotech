"""
Artifact Storage Task Executor

Store workflow outputs to object storage.
"""

import logging
from typing import Dict, Any
from datetime import datetime
import hashlib
import json
import uuid

try:
    import asyncpg
except ModuleNotFoundError:  # pragma: no cover - local unit tests may not install asyncpg
    asyncpg = None

from app.tasks import TaskExecutor
from app.settings import settings

logger = logging.getLogger(__name__)


class ArtifactStorageExecutor(TaskExecutor):
    """Store workflow artifacts to object storage"""

    _database_pool = None
    _database_pool_url = None
    
    @property
    def task_type(self) -> str:
        return "artifact_storage"
    
    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Store workflow output as artifact
        
        Step data should contain:
        - storage: storage type (object_store, database, local)
        - path_template: template for artifact path
        - content_field: field containing content to store
        - metadata: optional metadata to store with artifact
        """
        storage_type = step_data.get("storage", "object_store")
        content_field = step_data.get("content_field", "content")
        path_template = step_data.get("path_template", "artifacts/{workflow_id}/{timestamp}.json")
        
        # Get content to store
        previous_step = step_data.get("source_step") or self._get_previous_step_name(step_name)
        previous_result = workflow_state.get(previous_step, {})
        content = previous_result.get(content_field)
        
        if content is None:
            return {
                "success": False,
                "error": f"No content found in field '{content_field}'",
            }
        
        # Generate artifact path
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        artifact_path = path_template.format(
            workflow_id=workflow_id,
            timestamp=timestamp,
            tenant_id=workflow_state.get("tenant_id", "default"),
        )
        
        # Store based on storage type
        if storage_type == "local":
            result = await self._store_local(artifact_path, content)
        elif storage_type == "database":
            result = await self._store_database(workflow_id, artifact_path, content)
        else:  # object_store
            result = await self._store_object_store(artifact_path, content)
        
        return result
    
    async def _store_local(self, path: str, content: Any) -> Dict[str, Any]:
        """Store to local filesystem"""
        import os
        import json
        
        # Create directory if needed
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        
        # Write content
        try:
            with open(path, "w") as f:
                if isinstance(content, (dict, list)):
                    json.dump(content, f, indent=2)
                else:
                    f.write(str(content))
            
            logger.info(f"Stored artifact locally: {path}")
            
            return {
                "success": True,
                "storage_type": "local",
                "path": path,
                "size_bytes": os.path.getsize(path),
            }
            
        except Exception as e:
            logger.error(f"Local storage error: {e}")
            return {"success": False, "error": str(e)}
    
    async def _store_object_store(self, path: str, content: Any) -> Dict[str, Any]:
        """
        Store to object storage (Azure Blob, S3, or equivalent)

        In production, should use the active platform storage client.
        For now, mock the operation.
        """
        # Mock object storage - in production would actually upload
        content_str = str(content) if not isinstance(content, str) else content
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()[:16]
        
        logger.info(f"Stored artifact in object store: {path} (hash: {content_hash})")
        
        return {
            "success": True,
            "storage_type": "object_store",
            "path": path,
            "object_hash": content_hash,
            "mock": True,  # Indicates this is mocked
        }
    
    async def _store_database(
        self,
        workflow_id: str,
        path: str,
        content: Any,
    ) -> Dict[str, Any]:
        """Store to the orchestration database and return a durable artifact id."""
        if asyncpg is None:
            return {
                "success": False,
                "error": "asyncpg is required for database artifact storage",
            }

        artifact_id = str(uuid.uuid4())
        content_text = content if isinstance(content, str) else json.dumps(content, sort_keys=True)
        content_json = content if isinstance(content, (dict, list)) else None
        content_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()

        pool = await self._get_database_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS workflow_artifacts (
                    id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    artifact_path TEXT NOT NULL,
                    content_text TEXT NOT NULL,
                    content_json JSONB,
                    content_hash TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
            await conn.execute(
                """
                INSERT INTO workflow_artifacts (
                    id, workflow_id, artifact_path, content_text, content_json, content_hash
                ) VALUES ($1, $2, $3, $4, $5, $6)
                """,
                artifact_id,
                workflow_id,
                path,
                content_text,
                content_json,
                content_hash,
            )

        logger.info("Stored artifact in database: %s for workflow %s", path, workflow_id)

        return {
            "success": True,
            "storage_type": "database",
            "artifact_id": artifact_id,
            "path": path,
            "workflow_id": workflow_id,
            "content_hash": content_hash,
        }

    async def _get_database_pool(self):
        """Reuse the orchestration database pool instead of mocking the storage path."""
        database_url = settings.database_url
        if (
            self.__class__._database_pool is None
            or self.__class__._database_pool_url != database_url
        ):
            self.__class__._database_pool = await asyncpg.create_pool(
                database_url,
                min_size=1,
                max_size=3,
            )
            self.__class__._database_pool_url = database_url
        return self.__class__._database_pool
    
    def _get_previous_step_name(self, current_step: str) -> str:
        """Get the name of the previous step"""
        parts = current_step.rsplit("_", 1)
        if len(parts) > 1:
            return parts[0]
        return "previous"
