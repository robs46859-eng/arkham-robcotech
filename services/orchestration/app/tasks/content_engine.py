"""
ContentEngine task executors.

Bridges horizontal orchestration to ContentEngine agent capabilities:
- Content generation (articles, social, video scripts)
- AI-SEO optimization
- Programmatic SEO at scale
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

from app.tasks import TaskExecutor

SERVICE_ROOT = Path(__file__).resolve().parents[2]
MEDIA_COMMERCE_ROOT = SERVICE_ROOT.parent / "media-commerce"
if str(MEDIA_COMMERCE_ROOT) not in sys.path:
    sys.path.insert(0, str(MEDIA_COMMERCE_ROOT))

from app.agents.content_engine import ContentEngineAgent  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)


class ContentGenerationExecutor(TaskExecutor):
    """Generate content (articles, social, video scripts) using ContentEngine agent."""

    @property
    def task_type(self) -> str:
        return "content_generation"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        content_type = input_data.get("content_type", "article")
        topic = input_data.get("topic")
        keywords = input_data.get("keywords", [])
        target_word_count = input_data.get("target_word_count", 1000)

        if not tenant_id or not topic:
            return {
                "success": False,
                "error": "tenant_id and topic are required in workflow input_data",
            }

        agent = ContentEngineAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.generate_content(
            tenant_id=tenant_id,
            vertical=input_data.get("vertical", "media"),
            content_type=content_type,
            topic=topic,
            keywords=keywords,
            target_word_count=target_word_count,
        )

        logger.info("Content generated for workflow %s: %s (%s)", workflow_id, topic, content_type)
        return {
            "success": True,
            "content": result,
            "content_id": result.get("content_id"),
            "content_type": content_type,
            "word_count": result.get("word_count", 0),
            "quality_score": result.get("quality_score", 0),
        }


class AISeoOptimizationExecutor(TaskExecutor):
    """Optimize content for AI search engines using ContentEngine agent."""

    @property
    def task_type(self) -> str:
        return "ai_seo_optimization"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        content_id = input_data.get("content_id")
        content_text = input_data.get("content_text")

        if not tenant_id or not content_id:
            return {
                "success": False,
                "error": "tenant_id and content_id are required in workflow input_data",
            }

        agent = ContentEngineAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.optimize_for_ai_search(
            tenant_id=tenant_id,
            content_id=content_id,
            content_text=content_text,
        )

        logger.info("AI-SEO optimization complete for %s in workflow %s", content_id, workflow_id)
        return {
            "success": True,
            "optimization_result": result,
            "content_id": content_id,
            "ai_search_score": result.get("ai_search_score", 0),
            "recommendations_count": len(result.get("recommendations", [])),
            "optimizations_applied": result.get("optimizations_applied", []),
        }


class ProgrammaticSeoExecutor(TaskExecutor):
    """Generate programmatic SEO pages at scale using ContentEngine agent."""

    @property
    def task_type(self) -> str:
        return "programmatic_seo"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        tenant_id = workflow_state.get("tenant_id") or input_data.get("tenant_id")
        seed_keyword = input_data.get("seed_keyword")
        template_id = input_data.get("template_id")
        batch_size = input_data.get("batch_size", 10)

        if not tenant_id or not seed_keyword:
            return {
                "success": False,
                "error": "tenant_id and seed_keyword are required in workflow input_data",
            }

        agent = ContentEngineAgent(gateway_url=step_data.get("gateway_url", "http://localhost:8080"))
        result = await agent.generate_programmatic_seo_pages(
            tenant_id=tenant_id,
            vertical=input_data.get("vertical", "media"),
            seed_keyword=seed_keyword,
            template_id=template_id,
            batch_size=batch_size,
        )

        logger.info(
            "Programmatic SEO generated: %d pages for keyword '%s' in workflow %s",
            result.get("pages_generated", 0),
            seed_keyword,
            workflow_id,
        )
        return {
            "success": True,
            "programmatic_result": result,
            "pages_generated": result.get("pages_generated", 0),
            "keyword_cluster": result.get("keyword_cluster", []),
            "pages": result.get("pages", []),
        }
