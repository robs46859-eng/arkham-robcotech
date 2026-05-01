#!/usr/bin/env python3
"""ACA env/secrets agent for FullStackArkham.

Responsibilities:
- audit local secret exposure and missing production inputs
- persist canonical deployment secrets/config in Azure Key Vault
- apply Azure Container Apps secrets and env vars per service
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import string
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env.production"
AUDIT_REPORT = ROOT / "aca_env_secrets_audit.md"

POSTGRES_ADMIN_USER_SECRET = "postgres-admin-user"
POSTGRES_ADMIN_PASSWORD_SECRET = "postgres-admin-password"
DATABASE_URL_CORE_SECRET = "database-url-core"
DATABASE_URL_BIM_SECRET = "database-url-bim"
REDIS_URL_SECRET = "redis-url"
REDIS_PASSWORD_SECRET = "redis-password"
JWT_SECRET_SECRET = "jwt-secret"
STRIPE_SECRET_KEY_SECRET = "stripe-secret-key"
STRIPE_WEBHOOK_SECRET_SECRET = "stripe-webhook-secret"
STRIPE_PRICE_BASIC_SECRET = "stripe-price-id-basic"
STRIPE_PRICE_PRO_SECRET = "stripe-price-id-pro"
STRIPE_PRICE_ENTERPRISE_SECRET = "stripe-price-id-enterprise"
APPINSIGHTS_SECRET = "applicationinsights-connection-string"


EXTERNAL_SECRET_KEYS = {
    "STRIPE_SECRET_KEY": STRIPE_SECRET_KEY_SECRET,
    "STRIPE_WEBHOOK_SECRET": STRIPE_WEBHOOK_SECRET_SECRET,
    "STRIPE_PRICE_ID_BASIC": STRIPE_PRICE_BASIC_SECRET,
    "STRIPE_PRICE_ID_PRO": STRIPE_PRICE_PRO_SECRET,
    "STRIPE_PRICE_ID_ENTERPRISE": STRIPE_PRICE_ENTERPRISE_SECRET,
    "APPLICATIONINSIGHTS_CONNECTION_STRING": APPINSIGHTS_SECRET,
}


@dataclass(frozen=True)
class AppSpec:
    name: str
    base_plain_env: Dict[str, str]
    base_secret_env: Dict[str, str]
    dependency_env_keys: Tuple[str, ...] = ()
    optional_secret_env: Dict[str, str] = None


APP_SPECS: Dict[str, AppSpec] = {
    "gateway": AppSpec(
        name="gateway",
        base_plain_env={
            "SERVER_HOST": "0.0.0.0",
            "SERVER_PORT": "8080",
            "DATABASE_USER": "postgres",
            "DATABASE_NAME": "fullstackarkham",
            "DATABASE_PORT": "5432",
            "DATABASE_SSL_MODE": "require",
            "REDIS_PORT": "6380",
            "ARKHAM_ENABLED": "true",
        },
        base_secret_env={
            "DATABASE_PASSWORD": "dbpass",
            "REDIS_PASSWORD": "redispass",
            "JWT_SECRET": "jwtsecret",
        },
        dependency_env_keys=("ARKHAM_ENDPOINT",),
        optional_secret_env={
            "ANTHROPIC_API_KEY": "anthropic",
            "OPENAI_API_KEY": "openai",
            "GOOGLE_API_KEY": "google",
        },
    ),
    "arkham": AppSpec(
        name="arkham",
        base_plain_env={
            "DECEPTION_ENABLED": "true",
            "CROSS_TENANT_SHARE": "true",
        },
        base_secret_env={
            "DATABASE_URL": "dburl",
            "REDIS_URL": "redisurl",
        },
    ),
    "bim-ingestion": AppSpec(
        name="bim-ingestion",
        base_plain_env={
            "STORAGE_PATH": "/tmp/bim-storage",
        },
        base_secret_env={
            "DATABASE_URL": "dburlbim",
            "REDIS_URL": "redisurl",
        },
        dependency_env_keys=("GATEWAY_URL", "ORCHESTRATION_URL"),
    ),
    "orchestration": AppSpec(
        name="orchestration",
        base_plain_env={},
        base_secret_env={
            "DATABASE_URL": "dburl",
            "REDIS_URL": "redisurl",
        },
        dependency_env_keys=("GATEWAY_URL", "MEMORY_URL", "CACHE_URL"),
    ),
    "semantic-cache": AppSpec(
        name="semantic-cache",
        base_plain_env={},
        base_secret_env={
            "DATABASE_URL": "dburl",
            "REDIS_URL": "redisurl",
        },
    ),
    "memory": AppSpec(
        name="memory",
        base_plain_env={},
        base_secret_env={
            "DATABASE_URL": "dburl",
            "REDIS_URL": "redisurl",
        },
    ),
    "billing": AppSpec(
        name="billing",
        base_plain_env={
            "APP_DOMAIN": "robcotech.pro",
        },
        base_secret_env={
            "DATABASE_URL": "dburl",
        },
        optional_secret_env={
            "STRIPE_SECRET_KEY": "stripesk",
            "STRIPE_WEBHOOK_SECRET": "stripewh",
            "STRIPE_PRICE_ID_BASIC": "pricebasic",
            "STRIPE_PRICE_ID_PRO": "pricepro",
            "STRIPE_PRICE_ID_ENTERPRISE": "priceent",
            "APPLICATIONINSIGHTS_CONNECTION_STRING": "appinsights",
        },
    ),
    "media-commerce": AppSpec(
        name="media-commerce",
        base_plain_env={},
        base_secret_env={
            "DATABASE_URL": "dburl",
        },
        dependency_env_keys=("GATEWAY_URL", "ORCHESTRATION_URL"),
    ),
}


DEPENDENCY_TARGETS = {
    "gateway": {"ARKHAM_ENDPOINT": "arkham"},
    "bim-ingestion": {"GATEWAY_URL": "gateway", "ORCHESTRATION_URL": "orchestration"},
    "orchestration": {
        "GATEWAY_URL": "gateway",
        "MEMORY_URL": "memory",
        "CACHE_URL": "semantic-cache",
    },
    "media-commerce": {"GATEWAY_URL": "gateway", "ORCHESTRATION_URL": "orchestration"},
}


def run(cmd: List[str], capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=capture,
        check=False,
    )


def az(args: List[str], expect_json: bool = True):
    result = run(["az", *args])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "az command failed")
    if expect_json:
        text = result.stdout.strip()
        return json.loads(text) if text else {}
    return result.stdout.strip()


def load_env_file() -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not ENV_FILE.exists():
        return values
    for raw in ENV_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def is_placeholder(value: str | None) -> bool:
    if value is None:
        return True
    normalized = value.strip()
    if not normalized:
        return True
    markers = (
        "CHANGE_ME",
        "placeholder",
        "example",
        "your_",
        "sk_live_CHANGE_ME",
        "whsec_CHANGE_ME",
        "price_CHANGE_ME",
    )
    return any(marker.lower() in normalized.lower() for marker in markers)


def generate_secret(length: int = 48) -> str:
    alphabet = string.ascii_letters + string.digits + "-_"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def kv_secret_show(vault_name: str, secret_name: str) -> str | None:
    result = run(
        [
            "az",
            "keyvault",
            "secret",
            "show",
            "--vault-name",
            vault_name,
            "--name",
            secret_name,
            "--query",
            "value",
            "-o",
            "tsv",
        ]
    )
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def kv_secret_set(vault_name: str, secret_name: str, value: str) -> None:
    result = run(
        [
            "az",
            "keyvault",
            "secret",
            "set",
            "--vault-name",
            vault_name,
            "--name",
            secret_name,
            "--value",
            value,
            "--output",
            "none",
        ],
        capture=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to set secret {secret_name}")


def ensure_secret(vault_name: str, secret_name: str, desired_value: str | None) -> str:
    existing = kv_secret_show(vault_name, secret_name)
    if existing:
        return existing
    if desired_value is None:
        raise RuntimeError(f"missing required secret input for {secret_name}")
    kv_secret_set(vault_name, secret_name, desired_value)
    return desired_value


def get_external_secret_inputs() -> Dict[str, str]:
    env_file_values = load_env_file()
    resolved: Dict[str, str] = {}
    for env_key in EXTERNAL_SECRET_KEYS:
        candidate = os.getenv(env_key) or env_file_values.get(env_key)
        if candidate and not is_placeholder(candidate):
            resolved[env_key] = candidate
    return resolved


def sync_keyvault(args: argparse.Namespace) -> None:
    external_inputs = get_external_secret_inputs()
    pg_host = f"{args.postgres_server}.postgres.database.azure.com"
    redis_host = f"{args.redis_name}.redis.cache.windows.net"

    admin_user = ensure_secret(args.key_vault, POSTGRES_ADMIN_USER_SECRET, "postgres")
    admin_password = ensure_secret(
        args.key_vault,
        POSTGRES_ADMIN_PASSWORD_SECRET,
        generate_secret(),
    )

    redis_keys = az(
        [
            "redis",
            "list-keys",
            "--resource-group",
            args.resource_group,
            "--name",
            args.redis_name,
            "-o",
            "json",
        ]
    )
    redis_password = ensure_secret(
        args.key_vault,
        REDIS_PASSWORD_SECRET,
        redis_keys.get("primaryKey"),
    )

    core_db_url = (
        f"postgresql://{quote(admin_user)}:{quote(admin_password)}@{pg_host}:5432/"
        f"fullstackarkham?sslmode=require"
    )
    bim_db_url = (
        f"postgresql://{quote(admin_user)}:{quote(admin_password)}@{pg_host}:5432/"
        f"fullstackarkham_bim?sslmode=require"
    )
    redis_url = f"rediss://:{quote(redis_password)}@{redis_host}:6380/0"

    ensure_secret(args.key_vault, DATABASE_URL_CORE_SECRET, core_db_url)
    ensure_secret(args.key_vault, DATABASE_URL_BIM_SECRET, bim_db_url)
    ensure_secret(args.key_vault, REDIS_URL_SECRET, redis_url)
    ensure_secret(args.key_vault, JWT_SECRET_SECRET, generate_secret())

    for env_key, secret_name in EXTERNAL_SECRET_KEYS.items():
        value = external_inputs.get(env_key)
        if value:
            ensure_secret(args.key_vault, secret_name, value)

    print("Key Vault secrets synced.")


def build_audit_report(args: argparse.Namespace) -> str:
    env_file_values = load_env_file()
    external_inputs = get_external_secret_inputs()
    lines = ["# ACA Env/Secrets Audit", ""]

    if ENV_FILE.exists():
        lines.append(f"- `.env.production` exists at `{ENV_FILE}`.")
        exposed = []
        for env_key in EXTERNAL_SECRET_KEYS:
            raw = env_file_values.get(env_key)
            if raw and not is_placeholder(raw):
                exposed.append(env_key)
        if exposed:
            lines.append(
                f"- Plaintext secret exposure risk: `.env.production` contains live values for {', '.join(exposed)}."
            )
        else:
            lines.append("- `.env.production` currently looks like a template, not a live secret source.")
    else:
        lines.append("- `.env.production` is missing.")

    lines.append("- `scripts/launch.sh` is deprecated; the supported Azure flow is `scripts/deploy-bot.sh` with Key Vault-backed secret storage.")
    lines.append("- Service settings default many production connections to `localhost`, so ACA env wiring is mandatory.")

    missing = [key for key in EXTERNAL_SECRET_KEYS if key not in external_inputs]
    if missing:
        lines.append(f"- Missing external production inputs: {', '.join(missing)}.")
    else:
        lines.append("- All external production secret inputs were provided from env or `.env.production`.")

    if args.key_vault:
        lines.append("")
        lines.append("## Key Vault")
        for secret_name in [
            POSTGRES_ADMIN_USER_SECRET,
            POSTGRES_ADMIN_PASSWORD_SECRET,
            DATABASE_URL_CORE_SECRET,
            DATABASE_URL_BIM_SECRET,
            REDIS_URL_SECRET,
            REDIS_PASSWORD_SECRET,
            JWT_SECRET_SECRET,
            *EXTERNAL_SECRET_KEYS.values(),
        ]:
            status = "present" if kv_secret_show(args.key_vault, secret_name) else "missing"
            lines.append(f"- `{secret_name}`: {status}")

    return "\n".join(lines) + "\n"


def audit(args: argparse.Namespace) -> None:
    report = build_audit_report(args)
    AUDIT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_REPORT.write_text(report)
    print(report)


def kv_secret_values(vault_name: str) -> Dict[str, str]:
    names = [
        POSTGRES_ADMIN_USER_SECRET,
        POSTGRES_ADMIN_PASSWORD_SECRET,
        DATABASE_URL_CORE_SECRET,
        DATABASE_URL_BIM_SECRET,
        REDIS_URL_SECRET,
        REDIS_PASSWORD_SECRET,
        JWT_SECRET_SECRET,
        *EXTERNAL_SECRET_KEYS.values(),
    ]
    values = {}
    for name in names:
        value = kv_secret_show(vault_name, name)
        if value:
            values[name] = value
    return values


def containerapp_exists(resource_group: str, app_name: str) -> bool:
    result = run(
        ["az", "containerapp", "show", "--resource-group", resource_group, "--name", app_name, "-o", "json"]
    )
    return result.returncode == 0


def set_registry(resource_group: str, app_name: str, registry_server: str, username: str, password: str) -> None:
    result = run(
        [
            "az",
            "containerapp",
            "registry",
            "set",
            "--resource-group",
            resource_group,
            "--name",
            app_name,
            "--server",
            registry_server,
            "--username",
            username,
            "--password",
            password,
            "--output",
            "none",
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to set registry on {app_name}")


def set_secrets(resource_group: str, app_name: str, secret_pairs: Dict[str, str]) -> None:
    if not secret_pairs:
        return
    args = []
    for key, value in secret_pairs.items():
        args.append(f"{key}={value}")
    result = run(
        [
            "az",
            "containerapp",
            "secret",
            "set",
            "--resource-group",
            resource_group,
            "--name",
            app_name,
            "--secrets",
            *args,
            "--output",
            "none",
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to set secrets on {app_name}")


def set_env_vars(resource_group: str, app_name: str, env_pairs: Dict[str, str]) -> None:
    if not env_pairs:
        return
    args = [f"{key}={value}" for key, value in env_pairs.items()]
    result = run(
        [
            "az",
            "containerapp",
            "update",
            "--resource-group",
            resource_group,
            "--name",
            app_name,
            "--set-env-vars",
            *args,
            "--output",
            "none",
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to set env vars on {app_name}")


def fqdn_map(resource_group: str, app_names: List[str]) -> Dict[str, str]:
    mapping = {}
    for app_name in app_names:
        result = run(
            [
                "az",
                "containerapp",
                "show",
                "--resource-group",
                resource_group,
                "--name",
                app_name,
                "--query",
                "properties.configuration.ingress.fqdn",
                "-o",
                "tsv",
            ]
        )
        fqdn = result.stdout.strip()
        if fqdn:
            mapping[app_name] = f"https://{fqdn}"
    return mapping


def apply_containerapps(args: argparse.Namespace) -> None:
    secrets_by_name = kv_secret_values(args.key_vault)
    registry_creds = az(
        [
            "acr",
            "credential",
            "show",
            "--name",
            args.acr_name,
            "-o",
            "json",
        ]
    )
    registry_server = az(
        [
            "acr",
            "show",
            "--resource-group",
            args.resource_group,
            "--name",
            args.acr_name,
            "--query",
            "loginServer",
            "-o",
            "tsv",
        ],
        expect_json=False,
    )

    app_names = [args.app] if args.app else list(APP_SPECS.keys())
    fqdn_lookup = fqdn_map(args.resource_group, app_names) if args.phase == "dependencies" else {}

    for app_name in app_names:
        if not containerapp_exists(args.resource_group, app_name):
            print(f"Skipping missing container app: {app_name}", file=sys.stderr)
            continue

        spec = APP_SPECS[app_name]

        if args.phase == "base":
            print(f"[base] configuring {app_name}...", flush=True)
            set_registry(
                args.resource_group,
                app_name,
                registry_server,
                registry_creds["username"],
                registry_creds["passwords"][0]["value"],
            )
            secret_pairs = {}
            env_pairs = dict(spec.base_plain_env)

            if app_name == "gateway":
                env_pairs["DATABASE_HOST"] = f"{args.postgres_server}.postgres.database.azure.com"
                env_pairs["REDIS_HOST"] = f"{args.redis_name}.redis.cache.windows.net"

            for env_key, secret_alias in spec.base_secret_env.items():
                secret_name = {
                    "dburl": DATABASE_URL_CORE_SECRET,
                    "dburlbim": DATABASE_URL_BIM_SECRET,
                    "redisurl": REDIS_URL_SECRET,
                    "dbpass": POSTGRES_ADMIN_PASSWORD_SECRET,
                    "redispass": REDIS_PASSWORD_SECRET,
                    "jwtsecret": JWT_SECRET_SECRET,
                }[secret_alias]
                value = secrets_by_name.get(secret_name)
                if value:
                    secret_pairs[secret_alias] = value
                    env_pairs[env_key] = f"secretref:{secret_alias}"

            for env_key, secret_alias in (spec.optional_secret_env or {}).items():
                mapped_secret_name = {
                    "stripesk": STRIPE_SECRET_KEY_SECRET,
                    "stripewh": STRIPE_WEBHOOK_SECRET_SECRET,
                    "pricebasic": STRIPE_PRICE_BASIC_SECRET,
                    "pricepro": STRIPE_PRICE_PRO_SECRET,
                    "priceent": STRIPE_PRICE_ENTERPRISE_SECRET,
                    "appinsights": APPINSIGHTS_SECRET,
                    "anthropic": "anthropic-api-key",
                    "openai": "openai-api-key",
                    "google": "google-api-key",
                }.get(secret_alias)
                if not mapped_secret_name:
                    continue
                value = secrets_by_name.get(mapped_secret_name) or os.getenv(env_key)
                if value and not is_placeholder(value):
                    secret_pairs[secret_alias] = value
                    env_pairs[env_key] = f"secretref:{secret_alias}"

            set_secrets(args.resource_group, app_name, secret_pairs)
            set_env_vars(args.resource_group, app_name, env_pairs)
            print(f"[base] configured {app_name}", flush=True)
        else:
            print(f"[dependencies] configuring {app_name}...", flush=True)
            env_pairs = {}
            for env_key, target_app in DEPENDENCY_TARGETS.get(app_name, {}).items():
                target_url = fqdn_lookup.get(target_app)
                if target_url:
                    env_pairs[env_key] = target_url
            if env_pairs:
                set_env_vars(args.resource_group, app_name, env_pairs)
            print(f"[dependencies] configured {app_name}", flush=True)

    print(f"Applied {args.phase} container app configuration.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ACA env/secrets agent")
    sub = parser.add_subparsers(dest="command", required=True)

    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("--key-vault")
    audit_parser.set_defaults(func=audit)

    sync_parser = sub.add_parser("sync-keyvault")
    sync_parser.add_argument("--resource-group", required=True)
    sync_parser.add_argument("--key-vault", required=True)
    sync_parser.add_argument("--postgres-server", required=True)
    sync_parser.add_argument("--redis-name", required=True)
    sync_parser.set_defaults(func=sync_keyvault)

    apply_parser = sub.add_parser("apply-containerapps")
    apply_parser.add_argument("--resource-group", required=True)
    apply_parser.add_argument("--key-vault", required=True)
    apply_parser.add_argument("--postgres-server", required=True)
    apply_parser.add_argument("--redis-name", required=True)
    apply_parser.add_argument("--acr-name", required=True)
    apply_parser.add_argument("--phase", choices=("base", "dependencies"), required=True)
    apply_parser.add_argument("--app")
    apply_parser.set_defaults(func=apply_containerapps)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as exc:  # pragma: no cover - CLI
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
