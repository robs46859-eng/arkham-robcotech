#!/usr/bin/env python3
"""
FullStackArkham Auto-Deploy Agent

Runs continuously, fixing issues and retrying deployment until SUCCESS.
Has full permission to modify code, configs, and deployment scripts.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'

class AutoDeployAgent:
    """Autonomous deployment agent with full fix permissions"""

    def __init__(self):
        self.root = Path(__file__).resolve().parents[1]
        self.max_iterations = 10
        self.log_file = self.root / "deploy_agent.log"

    def log(self, message: str, level: str = "INFO"):
        """Log to both console and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": BLUE,
            "SUCCESS": GREEN,
            "WARNING": YELLOW,
            "ERROR": RED,
            "ACTION": CYAN,
        }
        color = colors.get(level, NC)
        
        console_msg = f"{color}[{timestamp}] [{level}] {message}{NC}"
        file_msg = f"[{timestamp}] [{level}] {message}"
        
        print(console_msg)
        
        with open(self.log_file, "a") as f:
            f.write(file_msg + "\n")

    def run_command(self, cmd: list, timeout: int = 300, check: bool = False) -> subprocess.CompletedProcess:
        """Run command and log output"""
        self.log(f"Running: {' '.join(cmd)}", "ACTION")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.root,
            timeout=timeout,
        )
        
        # Log output
        if result.stdout:
            with open(self.log_file, "a") as f:
                f.write(f"STDOUT:\n{result.stdout}\n")
        
        if result.stderr:
            with open(self.log_file, "a") as f:
                f.write(f"STDERR:\n{result.stderr}\n")
        
        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, cmd)
        
        return result

    def analyze_and_fix(self) -> bool:
        """Run debug agent to analyze and fix issues"""
        self.log("=" * 60, "INFO")
        self.log("PHASE 1: Analyze and Auto-Fix", "INFO")
        self.log("=" * 60, "INFO")

        result = self.run_command(
            ["python3", "scripts/debug_agent.py", "--analyze"],
            timeout=300,
        )

        # If analysis shows issues, run fix
        if "ISSUES FOUND" in result.stdout or result.returncode != 0:
            self.log("Issues detected, applying fixes...", "ACTION")
            fix_result = self.run_command(
                ["python3", "scripts/debug_agent.py", "--fix"],
                timeout=300,
            )
            return "READY FOR DEPLOY" in fix_result.stdout
        
        return "READY FOR DEPLOY" in result.stdout

    def validate_live(self) -> bool:
        """Run live E2E test"""
        self.log("=" * 60, "INFO")
        self.log("PHASE 2: Live E2E Validation", "INFO")
        self.log("=" * 60, "INFO")

        result = self.run_command(
            ["python3", "services/media-commerce/tests/test_live_e2e_all_verticals.py"],
            timeout=120,
        )

        if "8 passed, 0 failed" in result.stdout:
            self.log("✓ All 8 agents PASSED live test", "SUCCESS")
            return True
        
        self.log("Live E2E test FAILED", "ERROR")
        return False

    def deploy(self) -> bool:
        """Run deployment script"""
        self.log("=" * 60, "INFO")
        self.log("PHASE 3: Deploy to Azure", "INFO")
        self.log("=" * 60, "INFO")

        # Check Azure auth first
        self.log("Checking Azure authentication...", "ACTION")
        auth_result = self.run_command(
            ["az", "account", "show"],
            timeout=30,
        )

        if auth_result.returncode != 0:
            self.log("Azure authentication failed. Please run: az login", "ERROR")
            return False

        # Run deploy bot
        self.log("Starting deployment...", "ACTION")
        deploy_result = self.run_command(
            ["./scripts/deploy-bot.sh", "--deploy"],
            timeout=600,  # 10 minutes for deployment
        )

        # Check for success indicators
        success_indicators = [
            "Deployment complete",
            "All services deployed",
            "SUCCESS",
        ]

        for indicator in success_indicators:
            if indicator in deploy_result.stdout:
                self.log(f"✓ Deployment SUCCESS: {indicator}", "SUCCESS")
                return True

        # Check for specific errors that we can fix
        if "tag does not exist" in deploy_result.stdout:
            self.log("Docker tag issue detected, will retry...", "WARNING")
            return False
        
        if "Resource group" in deploy_result.stderr and "deleting" in deploy_result.stderr:
            self.log("Resource group still deleting, waiting...", "WARNING")
            time.sleep(30)
            return False

        self.log("Deployment did not complete successfully", "ERROR")
        return False

    def run(self):
        """Main deployment loop"""
        self.log("\n" + "=" * 60, "SUCCESS")
        self.log(" FULLSTACKARKHAM AUTO-DEPLOY AGENT", "SUCCESS")
        self.log(" Starting autonomous deployment sequence", "SUCCESS")
        self.log("=" * 60 + "\n", "SUCCESS")

        for iteration in range(1, self.max_iterations + 1):
            self.log(f"\n{'='*60}", "INFO")
            self.log(f" ITERATION {iteration}/{self.max_iterations}", "INFO")
            self.log(f"{'='*60}\n", "INFO")

            try:
                # Phase 1: Analyze and fix
                if not self.analyze_and_fix():
                    self.log("Analysis/fix phase failed, retrying...", "WARNING")
                    continue

                # Phase 2: Validate live
                if not self.validate_live():
                    self.log("Live validation failed, retrying...", "WARNING")
                    continue

                # Phase 3: Deploy
                if self.deploy():
                    self.log("\n" + "=" * 60, "SUCCESS")
                    self.log(" DEPLOYMENT COMPLETE - robcotech.pro IS LIVE!", "SUCCESS")
                    self.log("=" * 60 + "\n", "SUCCESS")
                    
                    # Final validation
                    self.final_validation()
                    return True
                
                self.log("Deployment failed, will retry after fixes...", "WARNING")
                time.sleep(10)

            except Exception as e:
                self.log(f"Error in iteration {iteration}: {e}", "ERROR")
                time.sleep(5)
                continue

        self.log("\n" + "=" * 60, "ERROR")
        self.log(f" MAX ITERATIONS ({self.max_iterations}) REACHED", "ERROR")
        self.log(" Deployment did not complete successfully", "ERROR")
        self.log(" Check deploy_agent.log for details", "ERROR")
        self.log("=" * 60 + "\n", "ERROR")

        return False

    def final_validation(self):
        """Post-deployment validation"""
        self.log("\n" + "=" * 60, "INFO")
        self.log("POST-DEPLOYMENT VALIDATION", "INFO")
        self.log("=" * 60, "INFO")

        # Run E2E test one more time
        result = self.run_command(
            ["python3", "services/media-commerce/tests/test_live_e2e_all_verticals.py"],
            timeout=120,
        )

        if "8 passed" in result.stdout:
            self.log("✓ Post-deployment validation: ALL AGENTS OPERATIONAL", "SUCCESS")
        else:
            self.log("⚠ Post-deployment validation: Some agents may need attention", "WARNING")


def main():
    agent = AutoDeployAgent()
    success = agent.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
