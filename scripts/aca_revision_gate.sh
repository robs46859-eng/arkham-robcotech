#!/usr/bin/env bash

set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-fullstackarkham-prod}"
ARTIFACT_DIR="${ARTIFACT_DIR:-artifacts/launch}"
APP_DOMAIN="${APP_DOMAIN:-robcotech.pro}"
API_DOMAIN="${API_DOMAIN:-api.${APP_DOMAIN}}"
SMOKE_TIMEOUT="${SMOKE_TIMEOUT:-12}"

APPS=(${APPS:-web gateway billing orchestration memory semantic-cache arkham media-commerce})
SMOKE_URLS=(${SMOKE_URLS:-https://${APP_DOMAIN} https://www.${APP_DOMAIN} https://${API_DOMAIN}/health})

MODE=""
SNAPSHOT_FILE=""

usage() {
  cat <<EOF
Usage: $0 --snapshot | --smoke | --gate <snapshot-file> | --rollback <snapshot-file> | --rollback-latest

Snapshots active Azure Container Apps revisions, runs production smoke checks,
and shifts traffic back to known-good revisions when a post-deploy gate fails.

Environment overrides:
  RESOURCE_GROUP    default: fullstackarkham-prod
  ARTIFACT_DIR      default: artifacts/launch
  APPS              default: web gateway billing orchestration memory semantic-cache arkham media-commerce
  SMOKE_URLS        default: frontend, www, api health
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --snapshot) MODE="snapshot" ;;
    --smoke) MODE="smoke" ;;
    --gate) MODE="gate"; SNAPSHOT_FILE="${2:-}"; shift ;;
    --rollback) MODE="rollback"; SNAPSHOT_FILE="${2:-}"; shift ;;
    --rollback-latest) MODE="rollback-latest" ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
  shift
done

if [ -z "$MODE" ]; then
  usage
  exit 1
fi

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

latest_active_revision() {
  local app_name=$1
  az containerapp revision list \
    --resource-group "$RESOURCE_GROUP" \
    --name "$app_name" \
    --query "sort_by([?properties.active], &properties.createdTime)[-1].name" \
    -o tsv
}

current_traffic_revision() {
  local app_name=$1
  local revision

  revision="$(az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$app_name" \
    --query "properties.configuration.ingress.traffic[?weight > \`0\` && revisionName != null][0].revisionName" \
    -o tsv 2>/dev/null || true)"

  if [ -n "$revision" ] && [ "$revision" != "null" ]; then
    echo "$revision"
    return
  fi

  latest_active_revision "$app_name"
}

snapshot_revisions() {
  require_cmd az
  mkdir -p "$ARTIFACT_DIR"

  local snapshot="${ARTIFACT_DIR}/known-good-revisions-$(date +%Y%m%d-%H%M%S).env"
  {
    echo "# Azure Container Apps known-good revision snapshot"
    echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "RESOURCE_GROUP=${RESOURCE_GROUP}"
  } > "$snapshot"

  for app_name in "${APPS[@]}"; do
    if az containerapp show --resource-group "$RESOURCE_GROUP" --name "$app_name" >/dev/null 2>&1; then
      echo "${app_name}=$(current_traffic_revision "$app_name")" >> "$snapshot"
    else
      echo "# ${app_name}=missing" >> "$snapshot"
    fi
  done

  echo "$snapshot"
}

run_smoke_checks() {
  require_cmd curl

  local failed=0
  for url in "${SMOKE_URLS[@]}"; do
    echo "Smoke: ${url}"
    if ! curl -fsS --max-time "$SMOKE_TIMEOUT" "$url" >/dev/null; then
      echo "FAILED: ${url}" >&2
      failed=1
    fi
  done

  return "$failed"
}

rollback_from_snapshot() {
  require_cmd az

  local snapshot=$1
  if [ ! -f "$snapshot" ]; then
    echo "Snapshot not found: $snapshot" >&2
    exit 1
  fi

  while IFS='=' read -r app_name revision; do
    case "$app_name" in
      ""|"#"*) continue ;;
      RESOURCE_GROUP) continue ;;
    esac

    if [ -z "${revision:-}" ]; then
      continue
    fi

    echo "Rolling ${app_name} back to ${revision}"
    az containerapp revision activate \
      --resource-group "$RESOURCE_GROUP" \
      --name "$app_name" \
      --revision "$revision" >/dev/null 2>&1 || true

    az containerapp ingress traffic set \
      --resource-group "$RESOURCE_GROUP" \
      --name "$app_name" \
      --revision-weight "${revision}=100"
  done < "$snapshot"
}

latest_snapshot() {
  find "$ARTIFACT_DIR" -name 'known-good-revisions-*.env' -type f | sort | tail -1
}

case "$MODE" in
  snapshot)
    snapshot_revisions
    ;;
  smoke)
    run_smoke_checks
    ;;
  gate)
    if [ -z "$SNAPSHOT_FILE" ]; then
      echo "--gate requires a snapshot file" >&2
      exit 1
    fi
    if run_smoke_checks; then
      echo "Smoke gate passed"
    else
      echo "Smoke gate failed; rolling back from ${SNAPSHOT_FILE}" >&2
      rollback_from_snapshot "$SNAPSHOT_FILE"
      exit 1
    fi
    ;;
  rollback)
    if [ -z "$SNAPSHOT_FILE" ]; then
      echo "--rollback requires a snapshot file" >&2
      exit 1
    fi
    rollback_from_snapshot "$SNAPSHOT_FILE"
    ;;
  rollback-latest)
    SNAPSHOT_FILE="$(latest_snapshot)"
    if [ -z "$SNAPSHOT_FILE" ]; then
      echo "No snapshot found in ${ARTIFACT_DIR}" >&2
      exit 1
    fi
    rollback_from_snapshot "$SNAPSHOT_FILE"
    ;;
esac
