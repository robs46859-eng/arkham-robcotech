# FullStackArkham Terraform Configuration
# Deploys infrastructure on Azure

terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  backend "azurerm" {
    resource_group_name  = var.resource_group_name
    storage_account_name = var.storage_account_name
    container_name       = var.container_name
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

# Variables
variable "resource_group_name" {
  description = "Azure Resource Group Name"
  type        = string
}

variable "storage_account_name" {
  description = "Azure Storage Account Name"
  type        = string
}

variable "container_name" {
  description = "Container Name for State Storage"
  type        = string
}

variable "location" {
  description = "Azure Location"
  type        = string
  default     = "East US"
}

# Local values
locals {
  name_prefix = "fsa-${var.environment}"
  labels = {
    project     = "fullstackarkham"
    environment = "prod"
    managed_by  = "terraform"
  }
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# Azure Container Apps Environment
resource "azurerm_container_app_environment" "app_environment" {
  name                = var.container_apps_env
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
}

# Azure Container App
resource "azurerm_container_app" "frontend" {
  name                = "${local.name_prefix}-frontend"
  resource_group_name = azurerm_resource_group.rg.name
  container_app_environment_id = azurerm_container_app_environment.app_environment.id
  revision_mode       = "single"

  identity {
    type = "SystemAssigned"
  }

  configuration {
    ingress {
      external = true
      target_port = 8080
    }
  }
}

# Add other necessary Azure resource configurations... 

# Outputs
output "frontend_url" {
  value = azurerm_container_app.frontend.configuration[0].ingress[0].fqdn
}
