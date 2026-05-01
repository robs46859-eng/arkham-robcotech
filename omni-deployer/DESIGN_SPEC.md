# DESIGN_SPEC.md - OmniDeployer Agent

## Overview
The OmniDeployer agent is a command-oriented assistant designed to simplify multi-platform deployments. It can execute shell commands, manage SSH sessions (for Hostinger), interact with Azure services, and handle GitHub repository operations (including GitHub Pages). 

## Core Capabilities
- **Command Execution**: Runs local shell commands for builds and system checks.
- **Multi-Platform Auth**: Manages credentials for Azure, Hostinger (SSH), and GitHub (PAT).
- **Git Operations**: Automatically handles staging, committing, and pushing to the `robs46859-eng` repository.

## Tools Required
- **ShellTool**: Local terminal execution for `npm run build`, etc.
- **SSHTool**: Remote command execution for Hostinger deployment tasks.
- **AzureCLITool**: Management of Azure DNS and static sites.
- **GitHubTool**: Repo management and GitHub Pages configuration.

## Constraints & Safety Rules
- **EXPLICIT APPROVAL**: The agent MUST NOT execute any modifying command (local or remote) without a direct confirmation ("Approved" or "Yes") from the user.
- **Credential Protection**: Never log or print plain-text secrets, SSH keys, or GitHub tokens.

## Success Criteria
- The agent can successfully push a local build to the `robs46859-eng` repository.
- The agent can SSH into Hostinger and restart a service or update files.
- Azure DNS records can be updated via the agent.
