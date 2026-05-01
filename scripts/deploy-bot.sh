#!/usr/bin/env bash

set -euo pipefail

RESOURCE_GROUP="robcotech-rg"
CONTAINER_APPS_ENV="robcotech-env"
FRONTEND_APP="web"
API_APP="gateway"
APP_DOMAIN="robcotech.pro"
API_DOMAIN="api.${APP_DOMAIN}"
WWW_DOMAIN="www.${APP_DOMAIN}"

echo "Deploying to Azure Container Apps..."

# Example deployment commands to Azure
az containerapp create \
  --name "$FRONTEND_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$CONTAINER_APPS_ENV" \
  --image "<IMAGE_URI>" \
  --target-port 8080 \
  --ingress "external" \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 0.5 \
  --memory 1.0Gi

az containerapp create \
  --name "$API_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$CONTAINER_APPS_ENV" \
  --image "<ANOTHER_IMAGE_URI>" \
  --target-port 8081 \
  --ingress "external" \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 0.5 \
  --memory 1.0Gi
