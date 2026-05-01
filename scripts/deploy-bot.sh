#!/bin/bash

# ============================================================================
# FullStackArkham Azure Deploy Bot
# Automated deployment for robcotech.pro
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
RESOURCE_GROUP="fullstackarkham-prod"
LOCATION="eastus"
POSTGRES_LOCATION="centralus"
ACR_NAME="fullstackarkhamacr"
CONTAINER_APPS_ENV="fullstackarkham-env"
APP_DOMAIN="robcotech.pro"
API_DOMAIN="api.${APP_DOMAIN}"
VERSION=$(git rev-parse --short HEAD)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
AZURE_AUTH_HOST="login.microsoftonline.com"
POSTGRES_SERVER_NAME="arkham-psql"
POSTGRES_SKU="Standard_B1ms"
POSTGRES_TIER="Burstable"
REDIS_NAME="arkham-redis"
KEY_VAULT_NAME=""
POSTGRES_FIREWALL_RULE_NAME="codex-deployer"
POSTGRES_AZURE_RULE_NAME="allow-azure-services"

# Services to deploy
# Format: app_name:source_path:container_port
SERVICES=(
    "web:apps/web:3000"
    "gateway:services/gateway:8080"
    "arkham:services/arkham:8080"
    "bim-ingestion:services/bim_ingestion:8080"
    "orchestration:services/orchestration:8080"
    "semantic-cache:services/semantic-cache:8080"
    "memory:services/memory:8080"
    "billing:services/billing:8080"
    "media-commerce:services/media-commerce:8087"
)

# ============================================================================
# Helper Functions
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

exit_with_error() {
    log_error "$1"
    exit 1
}

bootstrap_azure_context() {
    log_info "Loading Azure context from Azure CLI cache..."

    if [ -n "${AZURE_SUBSCRIPTION_ID:-}" ]; then
        az account set --subscription "$AZURE_SUBSCRIPTION_ID" >/dev/null
    fi

    export AZURE_SUBSCRIPTION_ID="$(az account show --query id -o tsv)"
    export AZURE_TENANT_ID="$(az account show --query tenantId -o tsv)"
    export AZURE_USER="$(az account show --query user.name -o tsv)"
    export ARM_SUBSCRIPTION_ID="$AZURE_SUBSCRIPTION_ID"
    export ARM_TENANT_ID="$AZURE_TENANT_ID"

    log_info "Using subscription: $AZURE_SUBSCRIPTION_ID"
    log_info "Using tenant: $AZURE_TENANT_ID"
    log_info "Using Azure user: $AZURE_USER"
}

resolve_azure_location() {
    if az group show --name "$RESOURCE_GROUP" --query location -o tsv >/dev/null 2>&1; then
        LOCATION="$(az group show --name "$RESOURCE_GROUP" --query location -o tsv)"
        log_info "Resolved Azure location from resource group: $LOCATION"
    else
        log_info "Using default Azure location: $LOCATION"
    fi
}

resolve_postgres_location() {
    if az postgres flexible-server show --resource-group "$RESOURCE_GROUP" --name "$POSTGRES_SERVER_NAME" --query location -o tsv >/dev/null 2>&1; then
        POSTGRES_LOCATION="$(az postgres flexible-server show --resource-group "$RESOURCE_GROUP" --name "$POSTGRES_SERVER_NAME" --query location -o tsv)"
    fi
    log_info "Using PostgreSQL location: $POSTGRES_LOCATION"
}

resolve_key_vault_name() {
    local existing_vault
    existing_vault="$(az keyvault list --resource-group "$RESOURCE_GROUP" --query '[0].name' -o tsv 2>/dev/null || true)"
    if [ -n "$existing_vault" ]; then
        KEY_VAULT_NAME="$existing_vault"
    else
        KEY_VAULT_NAME="fsarkhamkv${AZURE_SUBSCRIPTION_ID%%-*}"
    fi
    log_info "Using Key Vault name: $KEY_VAULT_NAME"
}

load_acr_credentials() {
    if ! az acr show --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" >/dev/null 2>&1; then
        exit_with_error "Azure Container Registry '$ACR_NAME' not found in resource group '$RESOURCE_GROUP'"
    fi

    export ACR_LOGIN_SERVER
    export ACR_USERNAME
    export ACR_PASSWORD
    ACR_LOGIN_SERVER="$(az acr show --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" --query loginServer -o tsv)"
    ACR_USERNAME="$(az acr credential show --name "$ACR_NAME" --query username -o tsv)"
    ACR_PASSWORD="$(az acr credential show --name "$ACR_NAME" --query passwords[0].value -o tsv)"
}

sync_key_vault_secrets() {
    log_info "Syncing deployment secrets into Key Vault..."
    python3 scripts/aca_env_secrets_agent.py sync-keyvault \
        --resource-group "$RESOURCE_GROUP" \
        --key-vault "$KEY_VAULT_NAME" \
        --postgres-server "$POSTGRES_SERVER_NAME" \
        --redis-name "$REDIS_NAME"
}

run_secrets_audit() {
    log_info "Running ACA env/secrets audit..."
    python3 scripts/aca_env_secrets_agent.py audit --key-vault "$KEY_VAULT_NAME"
}

get_kv_secret() {
    local secret_name=$1
    az keyvault secret show \
        --vault-name "$KEY_VAULT_NAME" \
        --name "$secret_name" \
        --query value \
        -o tsv
}

check_docker_daemon() {
    if ! docker info >/dev/null 2>&1; then
        if command -v colima >/dev/null 2>&1; then
            exit_with_error "Docker daemon is not reachable. Start Colima first with: colima start"
        fi
        exit_with_error "Docker daemon is not reachable. Start Docker Desktop or another local Docker runtime and retry."
    fi
}

ensure_postgres_firewall_rule() {
    local public_ip
    public_ip="$(curl -sS https://api.ipify.org)"
    if [ -z "$public_ip" ]; then
        exit_with_error "Unable to determine current public IP for PostgreSQL firewall access"
    fi

    local fw_help
    local use_new_firewall_syntax="false"
    fw_help="$(AZURE_CONFIG_DIR=/tmp/az-codex az postgres flexible-server firewall-rule create -h 2>/dev/null || true)"
    if printf '%s\n' "$fw_help" | grep -Eq '^[[:space:]]+--server-name([[:space:]]|$)'; then
        use_new_firewall_syntax="true"
    fi

    log_info "Ensuring PostgreSQL firewall rule for deploy host IP ${public_ip}..."
    if [ "$use_new_firewall_syntax" = "true" ]; then
        az postgres flexible-server firewall-rule create \
            --resource-group "$RESOURCE_GROUP" \
            --server-name "$POSTGRES_SERVER_NAME" \
            --name "$POSTGRES_FIREWALL_RULE_NAME" \
            --start-ip-address "$public_ip" \
            --end-ip-address "$public_ip" \
            --output table >/dev/null

        az postgres flexible-server firewall-rule create \
            --resource-group "$RESOURCE_GROUP" \
            --server-name "$POSTGRES_SERVER_NAME" \
            --name "$POSTGRES_AZURE_RULE_NAME" \
            --start-ip-address "0.0.0.0" \
            --end-ip-address "0.0.0.0" \
            --output table >/dev/null
    else
        az postgres flexible-server firewall-rule create \
            --resource-group "$RESOURCE_GROUP" \
            --name "$POSTGRES_SERVER_NAME" \
            --rule-name "$POSTGRES_FIREWALL_RULE_NAME" \
            --start-ip-address "$public_ip" \
            --end-ip-address "$public_ip" \
            --output table >/dev/null

        az postgres flexible-server firewall-rule create \
            --resource-group "$RESOURCE_GROUP" \
            --name "$POSTGRES_SERVER_NAME" \
            --rule-name "$POSTGRES_AZURE_RULE_NAME" \
            --start-ip-address "0.0.0.0" \
            --end-ip-address "0.0.0.0" \
            --output table >/dev/null
    fi
}

run_psql_in_docker() {
    local database_name=$1
    local sql_command=$2
    local admin_password
    admin_password="$(get_kv_secret "postgres-admin-password")"

    check_docker_daemon

    docker run --rm \
        -e PGPASSWORD="$admin_password" \
        postgres:16-alpine \
        psql \
        "host=${POSTGRES_SERVER_NAME}.postgres.database.azure.com port=5432 dbname=${database_name} user=postgres sslmode=require" \
        -v ON_ERROR_STOP=1 \
        -c "$sql_command"
}

run_sql_file_in_docker() {
    local database_name=$1
    local sql_file=$2
    local admin_password
    admin_password="$(get_kv_secret "postgres-admin-password")"

    check_docker_daemon

    docker run --rm \
        -e PGPASSWORD="$admin_password" \
        -v "$PWD/infra/docker/postgres:/sql:ro" \
        postgres:16-alpine \
        psql \
        "host=${POSTGRES_SERVER_NAME}.postgres.database.azure.com port=5432 dbname=${database_name} user=postgres sslmode=require" \
        -v ON_ERROR_STOP=1 \
        -f "/sql/${sql_file}"
}

postgres_table_exists() {
    local database_name=$1
    local table_name=$2
    local admin_password
    admin_password="$(get_kv_secret "postgres-admin-password")"

    check_docker_daemon

    docker run --rm \
        -e PGPASSWORD="$admin_password" \
        postgres:16-alpine \
        psql \
        "host=${POSTGRES_SERVER_NAME}.postgres.database.azure.com port=5432 dbname=${database_name} user=postgres sslmode=require" \
        -tA \
        -c "SELECT CASE WHEN to_regclass('public.${table_name}') IS NULL THEN '0' ELSE '1' END;" \
        | tr -d '[:space:]'
}

ensure_postgres_extensions_allowlist() {
    log_info "Allowlisting required PostgreSQL extensions on Azure server..."
    az postgres flexible-server parameter set \
        --resource-group "$RESOURCE_GROUP" \
        --server-name "$POSTGRES_SERVER_NAME" \
        --name azure.extensions \
        --value "uuid-ossp,pg_trgm,vector" \
        --output none
}

initialize_azure_databases() {
    log_info "Initializing Azure PostgreSQL databases and schema..."
    ensure_postgres_firewall_rule
    ensure_postgres_extensions_allowlist

    az postgres flexible-server db create \
        --resource-group "$RESOURCE_GROUP" \
        --server-name "$POSTGRES_SERVER_NAME" \
        --database-name fullstackarkham \
        --output table >/dev/null 2>&1 || true

    az postgres flexible-server db create \
        --resource-group "$RESOURCE_GROUP" \
        --server-name "$POSTGRES_SERVER_NAME" \
        --database-name fullstackarkham_bim \
        --output table >/dev/null 2>&1 || true

    local tenants_exists
    local subscription_plans_exists
    tenants_exists="$(postgres_table_exists "fullstackarkham" "tenants")"
    subscription_plans_exists="$(postgres_table_exists "fullstackarkham" "subscription_plans")"

    if [ "$tenants_exists" = "1" ] && [ "$subscription_plans_exists" != "1" ]; then
        log_warning "Detected partial core schema bootstrap; resuming remaining core schema steps..."
        run_sql_file_in_docker "fullstackarkham" "init-resume.sql"
    elif [ "$tenants_exists" = "1" ]; then
        log_info "Core schema already present; skipping init.sql"
    else
        run_sql_file_in_docker "fullstackarkham" "init.sql"
    fi

    local policies_exists
    policies_exists="$(postgres_table_exists "fullstackarkham" "policies")"

    if [ "$policies_exists" = "1" ]; then
        log_warning "Detected partial vertical schema bootstrap; resuming remaining vertical schema steps..."
        run_sql_file_in_docker "fullstackarkham" "init-verticals-resume.sql"
    else
        run_sql_file_in_docker "fullstackarkham" "init-verticals.sql"
    fi

    log_success "Azure PostgreSQL databases initialized"
}

reconcile_postgres_admin_password() {
    local admin_password
    admin_password="$(get_kv_secret "postgres-admin-password")"
    log_info "Reconciling PostgreSQL admin password with Key Vault..."
    az postgres flexible-server update \
        --resource-group "$RESOURCE_GROUP" \
        --name "$POSTGRES_SERVER_NAME" \
        --admin-password "$admin_password" \
        --yes \
        --output table >/dev/null
}

configure_containerapps_base() {
    log_info "Applying base ACA env/secrets configuration..."
    python3 scripts/aca_env_secrets_agent.py apply-containerapps \
        --resource-group "$RESOURCE_GROUP" \
        --key-vault "$KEY_VAULT_NAME" \
        --postgres-server "$POSTGRES_SERVER_NAME" \
        --redis-name "$REDIS_NAME" \
        --acr-name "$ACR_NAME" \
        --phase base
}

configure_containerapps_dependencies() {
    log_info "Applying ACA inter-service URL configuration..."
    python3 scripts/aca_env_secrets_agent.py apply-containerapps \
        --resource-group "$RESOURCE_GROUP" \
        --key-vault "$KEY_VAULT_NAME" \
        --postgres-server "$POSTGRES_SERVER_NAME" \
        --redis-name "$REDIS_NAME" \
        --acr-name "$ACR_NAME" \
        --phase dependencies
}

configure_frontend_runtime() {
    if ! az containerapp show --name web --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
        log_warning "Frontend Container App 'web' not found; skipping frontend runtime env"
        return
    fi

    local media_commerce_fqdn
    media_commerce_fqdn="$(az containerapp show \
        --name media-commerce \
        --resource-group "$RESOURCE_GROUP" \
        --query properties.configuration.ingress.fqdn \
        -o tsv 2>/dev/null || true)"
    if [ -z "$media_commerce_fqdn" ]; then
        media_commerce_fqdn="$API_DOMAIN"
    fi

    log_info "Applying frontend runtime configuration for ${APP_DOMAIN}..."
    az containerapp update \
        --name web \
        --resource-group "$RESOURCE_GROUP" \
        --set-env-vars \
            "APP_DOMAIN=${APP_DOMAIN}" \
            "API_DOMAIN=${API_DOMAIN}" \
            "APP_URL=https://${APP_DOMAIN}" \
            "API_URL=https://${API_DOMAIN}" \
            "GATEWAY_URL=https://${API_DOMAIN}" \
            "MEDIA_COMMERCE_URL=https://${media_commerce_fqdn}" \
            "NEXT_PUBLIC_ENABLE_ANALYTICS=false" \
        --output table >/dev/null
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Azure CLI
    if ! command -v az &> /dev/null; then
        exit_with_error "Azure CLI not installed. Install from: https://docs.microsoft.com/cli/azure/install-azure-cli"
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        exit_with_error "Docker not installed"
    fi
    check_docker_daemon
    
    # Check Azure login
    if ! az account show &> /dev/null; then
        exit_with_error "Not logged into Azure. Run: az login"
    fi

    if [ ! -f "scripts/aca_env_secrets_agent.py" ]; then
        exit_with_error "ACA env/secrets agent missing: scripts/aca_env_secrets_agent.py"
    fi

    bootstrap_azure_context
    resolve_azure_location
    resolve_postgres_location
    resolve_key_vault_name
    
    log_success "Prerequisites check passed"
}

check_azure_auth_connectivity() {
    log_info "Checking Azure authentication connectivity..."

    if ! python3 -c "import socket; socket.getaddrinfo('${AZURE_AUTH_HOST}', 443)" >/dev/null 2>&1; then
        exit_with_error "Cannot resolve ${AZURE_AUTH_HOST}. Azure setup/deploy needs working DNS/network access to Microsoft login endpoints. This is an external network/Azure issue, not a Docker Compose issue."
    fi

    if ! az account get-access-token >/dev/null 2>&1; then
        exit_with_error "Azure CLI is logged in but cannot fetch an access token. Check network access to Microsoft login endpoints or re-run 'az login'."
    fi

    log_success "Azure authentication connectivity check passed"
}

# ============================================================================
# Setup Functions
# ============================================================================

setup_infrastructure() {
    log_info "Setting up Azure infrastructure..."
    check_azure_auth_connectivity
    
    # Create resource group
    log_info "Creating resource group: $RESOURCE_GROUP"
    az group create \
        --name $RESOURCE_GROUP \
        --location $LOCATION \
        --output table
    
    if az acr show --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" >/dev/null 2>&1; then
        log_info "Container Registry already exists: $ACR_NAME"
    else
        log_info "Creating Container Registry: $ACR_NAME"
        az acr create \
            --resource-group "$RESOURCE_GROUP" \
            --name "$ACR_NAME" \
            --sku Basic \
            --admin-enabled true \
            --output table
    fi
    
    if az containerapp env show --name "$CONTAINER_APPS_ENV" --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
        log_info "Container Apps Environment already exists: $CONTAINER_APPS_ENV"
    else
        log_info "Creating Container Apps Environment: $CONTAINER_APPS_ENV"
        az containerapp env create \
            --name "$CONTAINER_APPS_ENV" \
            --resource-group "$RESOURCE_GROUP" \
            --location "$LOCATION" \
            --output table
    fi
    
    if az redis show --resource-group "$RESOURCE_GROUP" --name "$REDIS_NAME" >/dev/null 2>&1; then
        log_info "Redis Cache already exists: $REDIS_NAME"
    else
        log_info "Creating Redis Cache: $REDIS_NAME"
        az redis create \
            --name "$REDIS_NAME" \
            --resource-group "$RESOURCE_GROUP" \
            --location "$LOCATION" \
            --sku Basic \
            --vm-size c0 \
            --output table
    fi

    if az keyvault show --resource-group "$RESOURCE_GROUP" --name "$KEY_VAULT_NAME" >/dev/null 2>&1; then
        log_info "Key Vault already exists: $KEY_VAULT_NAME"
    else
        log_info "Creating Key Vault: $KEY_VAULT_NAME"
        az keyvault create \
            --name "$KEY_VAULT_NAME" \
            --resource-group "$RESOURCE_GROUP" \
            --location "$LOCATION" \
            --output table
    fi

    sync_key_vault_secrets

    if az postgres flexible-server show --resource-group "$RESOURCE_GROUP" --name "$POSTGRES_SERVER_NAME" >/dev/null 2>&1; then
        log_info "PostgreSQL Flexible Server already exists: $POSTGRES_SERVER_NAME"
    else
        log_info "Creating PostgreSQL Flexible Server: $POSTGRES_SERVER_NAME"
        az postgres flexible-server create \
            --resource-group "$RESOURCE_GROUP" \
            --name "$POSTGRES_SERVER_NAME" \
            --location "$POSTGRES_LOCATION" \
            --tier "$POSTGRES_TIER" \
            --sku-name "$POSTGRES_SKU" \
            --version 15 \
            --admin-user postgres \
            --admin-password "$(get_kv_secret "postgres-admin-password")" \
            --yes \
            --public-access Enabled \
            --output table
    fi

    reconcile_postgres_admin_password
    initialize_azure_databases
    run_secrets_audit
    
    log_success "Infrastructure setup complete"
    
    echo ""
    echo "Next steps:"
    echo "1. Review the ACA env/secrets audit at aca_env_secrets_audit.md"
    echo "2. Populate any still-missing external production secrets in Key Vault or environment"
    echo "3. Run deployment:"
    echo "   ./scripts/deploy-bot.sh --deploy"
}

# ============================================================================
# Build Functions
# ============================================================================

build_service() {
    local service_name=$1
    local service_path=$2
    
    log_info "Building $service_name..."
    
    if [ ! -f "$service_path/Dockerfile" ]; then
        log_warning "No Dockerfile found for $service_name, skipping..."
        return
    fi
    
    cd "$service_path"
    
    # Build image
    check_docker_daemon
    docker build \
        -t "${ACR_NAME}.azurecr.io/${service_name}:${VERSION}" \
        -t "${ACR_NAME}.azurecr.io/${service_name}:latest" \
        --platform linux/amd64 \
        --build-arg "APP_DOMAIN=${APP_DOMAIN}" \
        --build-arg "API_DOMAIN=${API_DOMAIN}" \
        --build-arg "APP_URL=https://${APP_DOMAIN}" \
        --build-arg "API_URL=https://${API_DOMAIN}" \
        --build-arg "GATEWAY_URL=https://${API_DOMAIN}" \
        --build-arg "MEDIA_COMMERCE_URL=https://${API_DOMAIN}" \
        .
    
    cd ../..
    
    log_success "Built $service_name"
}

build_all() {
    log_info "Building all services..."
    
    for service_entry in "${SERVICES[@]}"; do
        IFS=':' read -r service_name source_path _ <<< "$service_entry"
        build_service "$service_name" "$source_path"
    done
    
    log_success "All services built"
}

# ============================================================================
# Push Functions
# ============================================================================

push_all() {
    log_info "Pushing images to ACR..."
    check_azure_auth_connectivity
    load_acr_credentials
    check_docker_daemon
    
    # Login to ACR
    az acr login --name $ACR_NAME
    
    for service_entry in "${SERVICES[@]}"; do
        IFS=':' read -r service_name _ _ <<< "$service_entry"
        
        log_info "Pushing $service_name..."
        
        docker push "${ACR_NAME}.azurecr.io/${service_name}:${VERSION}"
        docker push "${ACR_NAME}.azurecr.io/${service_name}:latest"
    done
    
    log_success "All images pushed"
}

# ============================================================================
# Deploy Functions
# ============================================================================

deploy_service() {
    local service_name=$1
    local service_port=$2
    
    log_info "Deploying $service_name..."
    
    # Check if container app exists
    if az containerapp show --name $service_name --resource-group $RESOURCE_GROUP &> /dev/null; then
        az containerapp registry set \
            --name "$service_name" \
            --resource-group "$RESOURCE_GROUP" \
            --server "$ACR_LOGIN_SERVER" \
            --username "$ACR_USERNAME" \
            --password "$ACR_PASSWORD" \
            --output none

        # Update existing
        az containerapp update \
            --name $service_name \
            --resource-group $RESOURCE_GROUP \
            --image "${ACR_NAME}.azurecr.io/${service_name}:${VERSION}" \
            --output table
    else
        # Create new
        az containerapp create \
            --name $service_name \
            --resource-group $RESOURCE_GROUP \
            --environment $CONTAINER_APPS_ENV \
            --image "${ACR_NAME}.azurecr.io/${service_name}:${VERSION}" \
            --target-port $service_port \
            --ingress external \
            --registry-server "$ACR_LOGIN_SERVER" \
            --registry-username "$ACR_USERNAME" \
            --registry-password "$ACR_PASSWORD" \
            --cpu 0.25 \
            --memory 0.5Gi \
            --min-replicas 1 \
            --max-replicas 5 \
            --output table
    fi
    
    log_success "Deployed $service_name"
}

deploy_all() {
    log_info "Deploying all services..."
    check_azure_auth_connectivity
    load_acr_credentials
    
    for service_entry in "${SERVICES[@]}"; do
        IFS=':' read -r service_name _ service_port <<< "$service_entry"
        deploy_service "$service_name" "$service_port"
    done

    configure_containerapps_base
    configure_containerapps_dependencies
    configure_frontend_runtime
    
    log_success "All services deployed"
    
    echo ""
    echo "============================================================"
    echo "DEPLOYMENT COMPLETE"
    echo "============================================================"
    echo ""
    echo "Services deployed:"
    
    for service_entry in "${SERVICES[@]}"; do
        IFS=':' read -r service_name _ _ <<< "$service_entry"
        echo "  - https://${service_name}.${LOCATION}.azurecontainerapps.io"
    done
    
    echo ""
    echo "Frontend: https://web.${LOCATION}.azurecontainerapps.io"
    echo "Domain: run ./scripts/aca_dns_plan.sh --print for Hostinger records"
    echo ""
    echo "Monitor: Azure Portal → Container Apps"
    echo ""
}

# ============================================================================
# Status Functions
# ============================================================================

show_status() {
    log_info "Deployment status..."
    echo ""
    check_azure_auth_connectivity
    
    az containerapp list \
        --resource-group $RESOURCE_GROUP \
        --output table
    
    echo ""
    log_info "Recent deployments:"
    az containerapp revision list \
        --resource-group $RESOURCE_GROUP \
        --output table 2>/dev/null || echo "No revisions found"
}

show_logs() {
    local service_name=$1
    
    if [ -z "$service_name" ]; then
        log_error "Service name required. Usage: $0 --logs <service-name>"
        exit 1
    fi
    
    log_info "Streaming logs for $service_name..."
    check_azure_auth_connectivity
    
    az containerapp logs show \
        --name $service_name \
        --resource-group $RESOURCE_GROUP \
        --follow
}

# ============================================================================
# Cleanup Functions
# ============================================================================

cleanup() {
    log_warning "This will DELETE all Azure resources!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        log_info "Cleanup cancelled"
        exit 0
    fi
    
    log_info "Deleting resource group: $RESOURCE_GROUP"
    az group delete \
        --name $RESOURCE_GROUP \
        --yes \
        --no-wait
    
    log_success "Cleanup initiated (resources deleting in background)"
}

# ============================================================================
# Main
# ============================================================================

show_help() {
    echo "FullStackArkham Azure Deploy Bot"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  --setup       Create Azure infrastructure (one time, does not use Docker Compose)"
    echo "  --deploy      Build images locally and deploy all services to Azure"
    echo "  --status      Show deployment status"
    echo "  --logs <svc>  Stream logs for a service"
    echo "  --dns         Print Azure/Hostinger DNS records for custom domains"
    echo "  --snapshot    Snapshot current traffic revisions before a risky deploy"
    echo "  --smoke       Run production smoke checks"
    echo "  --rollback    Rollback to latest known-good revision snapshot"
    echo "  --cleanup     Delete all Azure resources"
    echo "  --help        Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 --setup"
    echo "  $0 --deploy"
    echo "  $0 --status"
    echo "  $0 --logs gateway"
}

main() {
    case "${1:-}" in
        --setup)
            check_prerequisites
            setup_infrastructure
            ;;
        --deploy)
            check_prerequisites
            sync_key_vault_secrets
            initialize_azure_databases
            run_secrets_audit
            build_all
            push_all
            deploy_all
            ;;
        --status)
            show_status
            ;;
        --dns)
            check_prerequisites
            ./scripts/aca_dns_plan.sh --print
            ;;
        --snapshot)
            check_prerequisites
            ./scripts/aca_revision_gate.sh --snapshot
            ;;
        --smoke)
            ./scripts/aca_revision_gate.sh --smoke
            ;;
        --logs)
            show_logs "$2"
            ;;
        --rollback)
            check_prerequisites
            ./scripts/aca_revision_gate.sh --rollback-latest
            ;;
        --cleanup)
            cleanup
            ;;
        --help|"")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
