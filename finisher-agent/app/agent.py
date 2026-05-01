from __future__ import annotations
import os
from pathlib import Path
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini

def read_project_status() -> str:
    """Read LAUNCH_LIST.md and ARCHITECTURE.md to determine progress."""
    root = Path(__file__).resolve().parent.parent.parent
    status = ""
    for filename in ["LAUNCH_LIST.md", "ARCHITECTURE.md"]:
        path = root / filename
        if path.exists():
            status += f"--- {filename} ---\n{path.read_text()}\n\n"
    return status or "No status documents found."

def identify_missing_features() -> str:
    """Identify unchecked items in LAUNCH_LIST.md."""
    status = read_project_status()
    missing = [line for line in status.splitlines() if "[ ]" in line]
    return "\n".join(missing) if missing else "All launch items appear to be checked!"

def generate_code_changes(file_path: str, new_content: str) -> str:
    """Generate a proposal for code changes. Actual file write happens after approval."""
    return f"PROPOSAL for {file_path}:\n\n{new_content}\n\nApply this change using 'apply_approved_change'."

def apply_approved_change(file_path: str, content: str) -> str:
    """Write the approved content to the specified file."""
    root = Path(__file__).resolve().parent.parent.parent
    target = root / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return f"Successfully updated {file_path}"

INSTRUCTION = """
You are the RobArkham Finisher Agent. Your goal is to drive this project to 100% completion based on the LAUNCH_LIST.md and ARCHITECTURE.md.

RESPONSIBILITIES:
1. Audit the repository against the launch criteria.
2. Propose code or configuration changes to fix missing items.
3. Only apply changes after explicit user approval of the proposal.
"""

root_agent = Agent(
    name="arkham_finisher_agent",
    model=Gemini(model="gemini-2.0-flash"),
    instruction=INSTRUCTION,
    tools=[read_project_status, identify_missing_features, generate_code_changes, apply_approved_change]
)

app = App(root_agent=root_agent, name="arkham_finisher_app")
