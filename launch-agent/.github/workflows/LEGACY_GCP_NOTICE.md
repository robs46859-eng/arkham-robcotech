# Legacy Workflow Notice

The GitHub Actions workflows in this directory were generated for a Google and Cloud Run deployment path.

They are deprecated for current Arkham operations.

## Current Rule

- Arkham production is Azure-first
- `launch-agent` is planning-only
- these workflows are not the authoritative CI/CD path

Do not wire production operations to these workflows without explicitly redesigning and re-approving them.

