# Debug Agent for FullStackArkham Build & Deploy

**Purpose:** Analyze build failures, fix code issues, and ensure all skills/tools are production-ready.

---

## Quick Start

```bash
cd /Users/joeiton/Desktop/FullStackArkham
python3 scripts/debug_agent.py --analyze
```

---

## What It Does

1. **Scans** all services for build errors
2. **Identifies** missing dependencies, syntax errors, config issues
3. **Auto-fixes** common issues (imports, paths, configs)
4. **Validates** all 8 vertical agents are functional
5. **Reports** detailed status with fix recommendations

---

## Usage

### Analyze All Services
```bash
python3 scripts/debug_agent.py --analyze
```

### Fix Issues Automatically
```bash
python3 scripts/debug_agent.py --fix
```

### Validate Specific Service
```bash
python3 scripts/debug_agent.py --service media-commerce
```

### Check Skills & Tools
```bash
python3 scripts/debug_agent.py --check-skills
```

### Full Build + Deploy Test
```bash
python3 scripts/debug_agent.py --full-test
```

---

## Output

```
========================================
 DEBUG AGENT REPORT
========================================

[✓] Gateway - PASS
[✓] Arkham - PASS
[✓] Orchestration - PASS
[✓] Memory - PASS
[✓] Semantic Cache - PASS
[✓] Billing - PASS
[✓] Media-Commerce - PASS

[✓] All 8 vertical agents functional
[✓] All skills loaded (40/40)
[✓] All workflows registered (29/29)
[✓] All executors registered (36/36)

BUILD STATUS: READY FOR DEPLOY
```

---

## Common Fixes Applied

| Issue | Auto-Fix |
|-------|----------|
| Missing imports | Adds import statements |
| Python path issues | Updates PYTHONPATH |
| Dockerfile errors | Fixes COPY/RUN commands |
| Config file missing | Creates from .example |
| Environment variables | Adds defaults to .env |
| Database schema | Runs migrations |

---

## Manual Intervention Required

The agent will flag these for manual review:
- Azure authentication issues
- DNS configuration
- Stripe API keys
- Database connection strings
- SSL certificates

---

## Files Modified

- `scripts/debug_agent.py` - Main debug agent
- `scripts/fix_imports.py` - Auto-fix Python imports
- `scripts/validate_skills.py` - Skill validation
- `scripts/check_dependencies.py` - Dependency checker

---

## Integration with Deploy Bot

```bash
# Run debug before deploy
python3 scripts/debug_agent.py --fix && ./scripts/deploy-bot.sh --deploy
```

---

**Created:** 2026-04-28  
**Version:** 1.0  
**Status:** Ready
