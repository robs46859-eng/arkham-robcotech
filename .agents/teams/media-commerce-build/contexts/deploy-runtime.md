# Deploy And Runtime Context

## Local Runtime
- `docker-compose.yml` is malformed: `media-commerce` is under `networks` instead of `services`
- this blocks a clean local validation path

## Deploy Bot
- `./scripts/deploy-bot.sh --setup` does not fail on Docker Compose
- it passes prerequisites
- it fails on the first Azure call because DNS/network resolution to `login.microsoftonline.com` fails during `az group create`

## Implication
- local compose/runtime repair is a repo fix
- Azure setup failure is currently an external network/state issue, not a compose issue

## Keep Separate
- local boot blockers
- Azure external provisioning blockers
