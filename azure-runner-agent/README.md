# azure-runner-agent

ADK-based Arkham deployment subagent for the Azure-first `robcotech.pro` stack.

## Project Structure

```
azure-runner-agent/
├── app/         # Core agent code
│   ├── agent.py               # Main agent logic
│   ├── fast_api_app.py        # FastAPI Backend server
│   └── app_utils/             # App utilities and helpers
├── tests/                     # Unit, integration, and load tests
├── GEMINI.md                  # AI-assisted development guide
└── pyproject.toml             # Project dependencies
```

> 💡 **Tip:** Use the local ADK development workflow for AI-assisted changes. Project-specific guidance is captured in `GEMINI.md`, including the requirement to stay on currently supported Gemini 2.x models rather than obsolete Gemini 1.5 variants.

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **agents-cli**: Agents CLI - Install with `uv tool install google-agents-cli`


## What It Does

- Reads the Arkham deployment contract from local repo docs and scripts
- Detects deployment drift such as stale `robcotech.pro` or GCP-era config
- Plans exact repo-scoped deployment actions around `./scripts/deploy-bot.sh`
- Runs only allowlisted repo commands, with explicit approval required for mutating actions

This package supports the repository deployment workflow. It does not replace the main deploy scripts or act as a separate production control plane.

## Quick Start

Install required packages:

```bash
agents-cli install
```

Inspect the local Arkham deployment state:

```bash
agents-cli run "Inspect the current Arkham deployment context and drift."
```

Open the ADK playground:

```bash
agents-cli playground
```

Run the FastAPI wrapper directly:

```bash
uv run uvicorn app.fast_api_app:app --host 0.0.0.0 --port 8000
```

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `agents-cli install` | Install dependencies using uv                                                         |
| `agents-cli run "..."` | Execute one Arkham deployment reasoning turn locally                                  |
| `agents-cli playground` | Launch local development environment                                                  |
| `agents-cli lint`    | Run code quality checks                                                               |
| `uv run pytest tests/unit/test_deployment_tools.py tests/integration/test_agent_definition.py` | Run the Arkham deployment smoke tests |

## Operating Rule

This package is approval-gated. It may inspect, plan, and execute only repo-scoped deployment commands that match the Arkham allowlist in `app/deployment_tools.py`.

---

## Development

Main files:

- `app/agent.py` - ADK root agent and safety instructions
- `app/deployment_tools.py` - Arkham deployment tools and allowlisted command execution
- `app/base_parameters.py` - deployment profile and command boundaries

Edit the agent logic and test with `agents-cli playground` or `agents-cli run`.

## Model Guidance

This package should be written and maintained against currently supported Gemini 2.x models. Do not add new instructions, examples, or fallback recommendations that depend on Gemini 1.5 model names.

## Deployment

Do not use this package as a standalone production deployment path. It should support the Azure-first repository workflow, not replace it.
