#!/usr/bin/env bash
# scripts/deploy-bot.sh
set -euo pipefail

RESOURCE_GROUP="fullstackarkham-prod"
CONTAINER_APPS_ENV="fullstackarkham-env"
ACR_NAME="fullstackarkhamacr"
FRONTEND_APP="web"
API_APP="gateway"
APP_DOMAIN="robcotech.pro"

echo "🚀 Starting Arkham Azure Deployment for $APP_DOMAIN..."

# 1. Login (Handled by orchestrator or assume existing session)
# 2. Get ACR Credentials
echo "🔑 Retrieving ACR credentials..."
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" -o tsv)
ACR_USER=$(az acr credential show --name "$ACR_NAME" --query "username" -o tsv)

# 3. Build and Push (Surgical: only Core Gateway and Web for now)
services=("gateway" "web" "arkham" "orchestration" "memory" "semantic-cache" "billing" "media-commerce" "bim-ingestion")

for service in "${services[@]}"; do
    echo "📦 Processing service: $service"
    IMAGE_TAG="${ACR_NAME}.azurecr.io/${service}:latest"
    
    # Simple build logic (assuming Dockerfile is in service dir or root)
    if [ "$service" == "web" ]; then
        context="apps/web"
    elif [[ "$service" == "gateway" || "$service" == "arkham" || "$service" == "orchestration" || "$service" == "memory" || "$service" == "semantic-cache" || "$service" == "billing" || "$service" == "media-commerce" || "$service" == "bim-ingestion" ]]; then
        context="services/${service}"
        # BIM ingestion has underscore in folder name
        if [ "$service" == "bim-ingestion" ]; then context="services/bim_ingestion"; fi
    fi

    echo "🏗️ Building $IMAGE_TAG from $context..."
    docker build -t "$IMAGE_TAG" "$context"
    
    echo "📤 Pushing $IMAGE_TAG..."
    docker push "$IMAGE_TAG"

    echo "🚀 Updating Container App: $service"
    # Port mapping
    port=8080
    case $service in
        web) port=3000 ;;
        gateway) port=8080 ;;
        arkham) port=8081 ;;
        bim-ingestion) port=8082 ;;
        orchestration) port=8083 ;;
        semantic-cache) port=8084 ;;
        memory) port=8085 ;;
        billing) port=8086 ;;
        media-commerce) port=8087 ;;
    esac

    az containerapp update \
      --name "$service" \
      --resource-group "$RESOURCE_GROUP" \
      --image "$IMAGE_TAG" \
      || az containerapp create \
        --name "$service" \
        --resource-group "$RESOURCE_GROUP" \
        --environment "$CONTAINER_APPS_ENV" \
        --image "$IMAGE_TAG" \
        --target-port "$port" \
        --ingress "external" \
        --min-replicas 0 \
        --max-replicas 1 \
        --cpu 0.25 \
        --memory 0.5Gi
done

echo "✅ Arkham Deployment Successful!"
