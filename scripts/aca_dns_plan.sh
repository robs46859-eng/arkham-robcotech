#!/usr/bin/env bash

set -euo pipefail

RESOURCE_GROUP="robcotech-rg"
CONTAINER_APPS_ENV="robcotech-env"
FRONTEND_APP="web"
API_APP="gateway"
APP_DOMAIN="robcotech.pro"
API_DOMAIN="api.${APP_DOMAIN}"
WWW_DOMAIN="www.${APP_DOMAIN}"
POLL_SECONDS="900"
POLL_INTERVAL="20"

MODE="print"

usage() {
  cat <<EOF
Usage: $0 [--print|--poll|--bind|--full]

Generates the Azure custom domains required for Azure Container Apps.

Environment overrides:
  RESOURCE_GROUP          default: robsotech-rg
  CONTAINER_APPS_ENV      default: robsotech-env
  FRONTEND_APP            default: web
  API_APP                 default: gateway
  APP_DOMAIN              default: robcotech.pro
EOF
}

# Remaining script logic...
