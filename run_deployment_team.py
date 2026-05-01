# run_deployment_team.py
import asyncio
import os
import subprocess
import httpx
from google.adk.agents import Agent, SequentialAgent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- Configuration ---
# Backed by Azure OpenAI via LiteLLM

os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT", "https://robco-omni-openai.openai.azure.com/")
os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"

# LiteLLM model string format for Azure
AZURE_MODEL = "azure/gpt-4" 

model = LiteLlm(model=AZURE_MODEL)

# Azure Service Principal Credentials (Resolved from environment)
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", "")

# --- Tools ---

def list_files(path: str = ".") -> dict:
    """Lists files in the repository."""
    try:
        return {"files": os.listdir(path)}
    except Exception as e:
        return {"error": str(e)}

def read_file(path: str) -> dict:
    """Reads a file's content."""
    try:
        with open(path, 'r') as f:
            return {"content": f.read()}
    except Exception as e:
        return {"error": str(e)}

def write_file(path: str, content: str) -> dict:
    """Writes content to a file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return {"status": f"Successfully wrote to {path}"}
    except Exception as e:
        return {"error": str(e)}

def run_deploy_script() -> dict:
    """Performs Azure login and runs the ./scripts/deploy-bot.sh --deploy command."""
    try:
        env = os.environ.copy()
        env["AZURE_TENANT_ID"] = AZURE_TENANT_ID
        env["AZURE_CLIENT_ID"] = AZURE_CLIENT_ID
        env["AZURE_CLIENT_SECRET"] = AZURE_CLIENT_SECRET
        env["AZURE_SUBSCRIPTION_ID"] = AZURE_SUBSCRIPTION_ID
        
        # Step 1: Login
        login_cmd = [
            "az", "login", "--service-principal",
            "-u", AZURE_CLIENT_ID,
            "-p", AZURE_CLIENT_SECRET,
            "--tenant", AZURE_TENANT_ID
        ]
        log_process = subprocess.run(login_cmd, capture_output=True, text=True, env=env)
        if log_process.returncode != 0:
            return {"error": f"Azure Login Failed: {log_process.stderr}"}
        
        # Step 2: Set Subscription
        sub_cmd = ["az", "account", "set", "--subscription", AZURE_SUBSCRIPTION_ID]
        subprocess.run(sub_cmd, env=env)

        # Step 3: Deploy
        # Note: Added --no-wait or similar if the script supports it, 
        # but here we wait to confirm success.
        process = subprocess.Popen(
            ["bash", "./scripts/deploy-bot.sh", "--deploy"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env
        )
        
        output = []
        for line in process.stdout:
            print(line, end="") 
            output.append(line)
        
        process.wait()
        
        return {
            "exit_code": process.returncode,
            "output": "".join(output[-100:]) # Return more context
        }
    except Exception as e:
        return {"error": str(e)}

async def verify_deployment(url: str) -> dict:
    """Verifies the deployment by hitting the health endpoint."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            return {
                "status_code": response.status_code,
                "content_preview": response.text[:200]
            }
    except Exception as e:
        return {"error": str(e)}

# --- Agents ---

reviewer = Agent(
    name="reviewer",
    model=model,
    instruction="""You are the Arkham Reviewer. 
    Analyze the current repository state. Ensure stelar.host has been replaced by robcotech.pro.
    Verify that the credentials provided are present in .env.production.
    Check for any remaining GCP/GCS drift in the core services and deployment scripts.""",
    tools=[list_files, read_file],
    output_key="review_report"
)

fixer = Agent(
    name="fixer",
    model=model,
    instruction="""You are the Arkham Fixer.
    Based on the review_report: {review_report}, apply any final fixes needed to standardise the deployment on Azure for robcotech.pro.
    Ensure all scripts use the correct Azure-first authoritative paths.
    Standardize ACR_NAME, RESOURCE_GROUP, and other Azure variables if they still reference 'stelar'.""",
    tools=[read_file, write_file],
    output_key="fix_summary"
)

deployer = Agent(
    name="deployer",
    model=model,
    instruction="""You are the Arkham Deployer.
    Execute the deployment using run_deploy_script.
    Monitor the output. If it fails, analyze the error and communicate it.
    You must NOT stop until you confirm the deployment script has finished successfully (Exit Code 0).""",
    tools=[run_deploy_script],
    output_key="deployment_status"
)

verifier = Agent(
    name="verifier",
    model=model,
    instruction="""You are the Arkham Verifier.
    Once deployment_status reports success, verify the endpoints:
    - https://robcotech.pro
    - https://api.robcotech.pro
    Provide a final comprehensive report of the fixes, the deployment process, and the final health status.""",
    tools=[verify_deployment, read_file],
)

team = SequentialAgent(
    name="azure_deployment_team",
    sub_agents=[reviewer, fixer, deployer, verifier],
)

app = App(root_agent=team, name="arkham_deploy_app")

async def main():
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="arkham_deploy_app", user_id="admin", session_id="s1")
    runner = Runner(app=app, session_service=session_service)
    
    print("--- Starting Azure Multi-Agent Deployment Team (Azure OpenAI Backed) ---")
    async for event in runner.run_async(
        user_id="admin", 
        session_id="s1",
        new_message=types.Content(role="user", parts=[types.Part.from_text(text="Execute the full review, fix, and deployment for robcotech.pro on Azure.")])
    ):
        if event.is_final_response():
            print("\n--- FINAL REPORT ---")
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
