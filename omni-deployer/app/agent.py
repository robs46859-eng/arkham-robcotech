# ruff: noqa
# Copyright 2026 Google LLC

import os
import subprocess
import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

# --- Environment Setup ---
_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# --- OmniDeployer Tools ---

def run_local_command(command: str) -> str:
    """
    Executes a local shell command. Use this for building projects, 
    running local scripts, or system diagnostics.
    
    Args:
        command: The full shell command to execute.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return f"Output:\n{result.stdout}\nErrors:\n{result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"Command failed with exit code {e.returncode}.\nOutput:\n{e.stdout}\nErrors:\n{e.stderr}"

def run_remote_ssh(host: str, username: str, command: str) -> str:
    """
    Executes a command on a remote server via SSH. Use this for 
    Hostinger or other remote server deployments.
    
    Args:
        host: The IP address or hostname of the remote server.
        username: The SSH username.
        command: The command to execute on the remote host.
    """
    ssh_cmd = f"ssh {username}@{host} '{command}'"
    return run_local_command(ssh_cmd)

def github_operation(repo_name: str, action: str, commit_message: str = "") -> str:
    """
    Handles GitHub operations such as creating repos, pushing code, or 
    configuring GitHub Pages.
    
    Args:
        repo_name: The name of the repository (e.g., 'robs46859-eng').
        action: One of 'push', 'create', 'status', 'deploy-pages'.
        commit_message: Optional message for 'push' action.
    """
    if action == "push":
        cmd = f"git add . && git commit -m '{commit_message}' && git push origin main"
    elif action == "status":
        cmd = "git status"
    elif action == "create":
        cmd = f"gh repo create {repo_name} --public --source=. --remote=origin --push"
    elif action == "deploy-pages":
        cmd = "gh pages deploy"
    else:
        return f"Action '{action}' not recognized."
    
    return run_local_command(cmd)

def azure_cli_command(command: str) -> str:
    """
    Executes an Azure CLI command. Use this for managing DNS or static sites.
    
    Args:
        command: The full 'az' command (e.g., 'az network dns record-set a add-record ...').
    """
    if not command.startswith("az"):
        command = f"az {command}"
    return run_local_command(command)

# --- Agent Definition ---

OMNI_INSTRUCTION = """
You are OmniDeployer, a senior deployment engineer. 
Your primary goal is to simplify deployments across Hostinger, Azure, and GitHub.

### CORE OPERATIONAL RULES:
1. **NO ACT WITHOUT APPROVAL**: You MUST NOT execute any modifying tool (run_local_command, run_remote_ssh, github_operation, azure_cli_command) without presenting the EXACT command to the user and receiving explicit approval (e.g., "Yes", "Approve", "Go ahead").
2. **PLAN BEFORE ACTING**: For complex tasks, outline the steps you intend to take first.
3. **SECURITY**: Never ask for or print passwords/tokens in plain text. Assume the environment is configured with necessary CLI auth (gh, az) and SSH keys.

### WORKFLOW:
- When a user asks to deploy, construct the necessary commands.
- Present them to the user: "I am ready to run: [command]. Should I proceed?"
- Only after approval, execute the tool.
"""

root_agent = Agent(
    name="omni_deployer",
    model=Gemini(
        model="gemini-2.0-flash",  # Updated to Gemini 2.0 Flash
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=OMNI_INSTRUCTION,
    tools=[run_local_command, run_remote_ssh, github_operation, azure_cli_command],
)

app = App(
    root_agent=root_agent,
    name="omni_deployer_app",
)
