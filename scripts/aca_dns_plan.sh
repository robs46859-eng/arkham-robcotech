#!/usr/bin/env bash

set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-fullstackarkham-prod}"
CONTAINER_APPS_ENV="${CONTAINER_APPS_ENV:-fullstackarkham-env}"
FRONTEND_APP="${FRONTEND_APP:-web}"
API_APP="${API_APP:-gateway}"
APP_DOMAIN="${APP_DOMAIN:-robcotech.pro}"
API_DOMAIN="${API_DOMAIN:-api.${APP_DOMAIN}}"
WWW_DOMAIN="${WWW_DOMAIN:-www.${APP_DOMAIN}}"
POLL_SECONDS="${POLL_SECONDS:-900}"
POLL_INTERVAL="${POLL_INTERVAL:-20}"

MODE="print"

usage() {
  cat <<EOF
Usage: $0 [--print|--poll|--bind|--full]

Generates the Hostinger DNS records required for Azure Container Apps custom
domains, optionally polls propagation, and optionally binds Azure managed certs.

Environment overrides:
  RESOURCE_GROUP          default: fullstackarkham-prod
  CONTAINER_APPS_ENV      default: fullstackarkham-env
  FRONTEND_APP            default: web
  API_APP                 default: gateway
  APP_DOMAIN              default: robcotech.pro
  POLL_SECONDS            default: 900
  POLL_INTERVAL           default: 20
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --print) MODE="print" ;;
    --poll) MODE="poll" ;;
    --bind) MODE="bind" ;;
    --full) MODE="full" ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
  shift
done

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

load_azure_values() {
  require_cmd az

  ENV_STATIC_IP="$(az containerapp env show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$CONTAINER_APPS_ENV" \
    --query properties.staticIp \
    -o tsv)"

  FRONTEND_FQDN="$(az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$FRONTEND_APP" \
    --query properties.configuration.ingress.fqdn \
    -o tsv)"

  API_FQDN="$(az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$API_APP" \
    --query properties.configuration.ingress.fqdn \
    -o tsv)"

  FRONTEND_VERIFY_ID="$(az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$FRONTEND_APP" \
    --query properties.customDomainVerificationId \
    -o tsv)"

  API_VERIFY_ID="$(az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$API_APP" \
    --query properties.customDomainVerificationId \
    -o tsv)"
}

print_records() {
  cat <<EOF
Hostinger records to create or update for ${APP_DOMAIN}

Frontend apex:
  Type: A
  Name: @
  Value: ${ENV_STATIC_IP}
  TTL: lowest available

Frontend apex Azure validation:
  Type: TXT
  Name: asuid
  Value: ${FRONTEND_VERIFY_ID}
  TTL: lowest available

Frontend www:
  Type: CNAME
  Name: www
  Value: ${FRONTEND_FQDN}
  TTL: lowest available

Frontend www Azure validation:
  Type: TXT
  Name: asuid.www
  Value: ${FRONTEND_VERIFY_ID}
  TTL: lowest available

API gateway:
  Type: CNAME
  Name: api
  Value: ${API_FQDN}
  TTL: lowest available

API gateway Azure validation:
  Type: TXT
  Name: asuid.api
  Value: ${API_VERIFY_ID}
  TTL: lowest available

CAA note:
  If Hostinger already has CAA records for ${APP_DOMAIN}, add/confirm:
  Type: CAA
  Name: @
  Value: 0 issue "digicert.com"
EOF
}

dig_value() {
  local type=$1
  local name=$2
  dig +short "$type" "$name" 2>/dev/null | sed 's/\.$//' | tr -d '"'
}

wait_for_record() {
  local type=$1
  local name=$2
  local expected=$3
  local deadline=$((SECONDS + POLL_SECONDS))

  echo "Waiting for ${type} ${name} -> ${expected}"
  while [ "$SECONDS" -lt "$deadline" ]; do
    if dig_value "$type" "$name" | grep -Fqx "$expected"; then
      echo "OK: ${type} ${name}"
      return 0
    fi
    sleep "$POLL_INTERVAL"
  done

  echo "Timed out waiting for ${type} ${name}" >&2
  echo "Current value(s):" >&2
  dig_value "$type" "$name" >&2 || true
  return 1
}

poll_records() {
  require_cmd dig
  wait_for_record A "$APP_DOMAIN" "$ENV_STATIC_IP"
  wait_for_record TXT "asuid.${APP_DOMAIN}" "$FRONTEND_VERIFY_ID"
  wait_for_record CNAME "$WWW_DOMAIN" "$FRONTEND_FQDN"
  wait_for_record TXT "asuid.${WWW_DOMAIN}" "$FRONTEND_VERIFY_ID"
  wait_for_record CNAME "$API_DOMAIN" "$API_FQDN"
  wait_for_record TXT "asuid.${API_DOMAIN}" "$API_VERIFY_ID"
}

bind_hostname() {
  local app_name=$1
  local hostname=$2
  local validation_method=$3

  echo "Adding hostname ${hostname} to ${app_name}..."
  az containerapp hostname add \
    --resource-group "$RESOURCE_GROUP" \
    --name "$app_name" \
    --hostname "$hostname" >/dev/null 2>&1 || true

  echo "Binding managed certificate for ${hostname}..."
  az containerapp hostname bind \
    --resource-group "$RESOURCE_GROUP" \
    --name "$app_name" \
    --environment "$CONTAINER_APPS_ENV" \
    --hostname "$hostname" \
    --validation-method "$validation_method"
}

bind_domains() {
  bind_hostname "$FRONTEND_APP" "$APP_DOMAIN" HTTP
  bind_hostname "$FRONTEND_APP" "$WWW_DOMAIN" CNAME
  bind_hostname "$API_APP" "$API_DOMAIN" CNAME
}

load_azure_values

case "$MODE" in
  print)
    print_records
    ;;
  poll)
    print_records
    poll_records
    ;;
  bind)
    bind_domains
    ;;
  full)
    print_records
    poll_records
    bind_domains
    ;;
esac
