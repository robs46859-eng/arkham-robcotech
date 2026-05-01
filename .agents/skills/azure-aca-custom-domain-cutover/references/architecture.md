# Architecture References

Read first:
- `ARCHITECTURE.md`

Primary deployment surfaces:
- frontend app: `apps/web`
- public API ingress: `services/gateway`
- deployment script: `scripts/deploy-bot.sh`

Public routing target from architecture:
- `https://robcotech.pro` -> frontend
- `https://www.robcotech.pro` -> frontend alias
- `https://api.robcotech.pro` -> gateway / API ingress
