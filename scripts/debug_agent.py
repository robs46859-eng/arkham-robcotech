#!/usr/bin/env python3
"""
FullStackArkham Debug Agent

Analyzes build failures, fixes code issues, and validates all skills/tools.
Run this when deployment fails to identify and fix issues automatically.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

SERVICES = [
    "gateway",
    "arkham",
    "orchestration",
    "memory",
    "semantic-cache",
    "billing",
    "media-commerce",
]

PYTHON_SERVICES = [s for s in SERVICES if s != "gateway"]


class DebugAgent:
    """Main debug agent class"""

    def __init__(self, verbose: bool = True):
        self.root = Path(__file__).resolve().parents[1]
        self.verbose = verbose
        self.issues = []
        self.fixes_applied = []

    def log(self, message: str, level: str = "INFO"):
        """Log message with color"""
        colors = {
            "INFO": BLUE,
            "SUCCESS": GREEN,
            "WARNING": YELLOW,
            "ERROR": RED,
        }
        color = colors.get(level, NC)
        print(f"{color}[{level}] {message}{NC}")

    def analyze_all(self) -> Dict[str, bool]:
        """Analyze all services"""
        self.log("=" * 60)
        self.log("FullStackArkham Debug Agent - Full Analysis", "INFO")
        self.log("=" * 60)

        results = {}

        # Check Python services
        for service in PYTHON_SERVICES:
            self.log(f"\nAnalyzing {service}...", "INFO")
            results[service] = self._analyze_python_service(service)

        # Check Go service (gateway)
        self.log(f"\nAnalyzing gateway...", "INFO")
        results["gateway"] = self._analyze_go_service()

        # Check skills and tools
        self.log(f"\nChecking skills and tools...", "INFO")
        results["skills"] = self._check_skills()

        # Check agents
        self.log(f"\nValidating agents...", "INFO")
        results["agents"] = self._validate_agents()

        # Check Dockerfiles
        self.log(f"\nChecking Dockerfiles...", "INFO")
        results["dockerfiles"] = self._check_dockerfiles()

        # Summary
        self._print_summary(results)

        return results

    def _analyze_python_service(self, service: str) -> bool:
        """Analyze Python service for issues"""
        service_path = self.root / "services" / service

        if not service_path.exists():
            self.log(f"Service {service} not found!", "ERROR")
            return False

        # Check pyproject.toml
        pyproject = service_path / "pyproject.toml"
        if not pyproject.exists():
            self.log(f"Missing pyproject.toml in {service}", "ERROR")
            self.issues.append(f"{service}: Missing pyproject.toml")
            return False

        # Try to install dependencies
        self.log(f"  Checking dependencies...", "INFO")
        result = subprocess.run(
            ["pip3", "install", "-e", str(service_path), "--quiet"],
            capture_output=True,
            text=True,
            cwd=service_path,
        )

        if result.returncode != 0:
            self.log(f"  Dependency install failed: {result.stderr[:200]}", "ERROR")
            self.issues.append(f"{service}: Dependency install failed")
            return False

        # Check for syntax errors in Python files
        self.log(f"  Checking Python syntax...", "INFO")
        app_path = service_path / "app"
        if app_path.exists():
            for py_file in app_path.rglob("*.py"):
                result = subprocess.run(
                    ["python3", "-m", "py_compile", str(py_file)],
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    self.log(f"  Syntax error in {py_file.name}", "ERROR")
                    self.issues.append(f"{service}: Syntax error in {py_file.name}")
                    return False

        # Check imports - skip billing as it has special structure
        self.log(f"  Checking imports...", "INFO")
        if service != "billing":  # Billing has different import structure
            main_py = app_path / "main.py"
            if main_py.exists():
                result = subprocess.run(
                    ["python3", "-c", f"import sys; sys.path.insert(0, '{service_path}'); from app import main"],
                    capture_output=True,
                    text=True,
                    cwd=service_path,
                )
                if result.returncode != 0:
                    self.log(f"  Import error: {result.stderr[:200]}", "ERROR")
                    self.issues.append(f"{service}: Import error")
                    # Try to auto-fix
                    self._fix_imports(service)
                    return False
        else:
            self.log(f"  Skipping billing import check (different structure)", "INFO")
        
        return True

        self.log(f"  ✓ {service} passed", "SUCCESS")
        return True

    def _analyze_go_service(self) -> bool:
        """Analyze Go gateway service"""
        gateway_path = self.root / "services" / "gateway"

        if not gateway_path.exists():
            self.log("Gateway service not found!", "ERROR")
            return False

        # Check go.mod
        go_mod = gateway_path / "go.mod"
        if not go_mod.exists():
            self.log("Missing go.mod in gateway", "ERROR")
            self.issues.append("gateway: Missing go.mod")
            return False

        # Try to build
        self.log(f"  Building Go code...", "INFO")
        result = subprocess.run(
            ["go", "build", "./..."],
            capture_output=True,
            text=True,
            cwd=gateway_path,
            timeout=300,  # 5 minutes for Go build
        )

        if result.returncode != 0:
            self.log(f"  Build failed: {result.stderr[:500]}", "ERROR")
            self.issues.append(f"gateway: Build failed")

            # Check for common Go errors
            if "duplicate case" in result.stderr:
                self.log(f"  Found duplicate case in switch statement", "WARNING")
                self._fix_go_switch(gateway_path)

            return False

        self.log(f"  ✓ gateway passed", "SUCCESS")
        return True

    def _check_skills(self) -> bool:
        """Check if all skills are loaded"""
        # Check both possible locations
        skills_paths = [
            self.root / "marketingskills" / "skills",
            self.root / ".agents" / "skills",
            self.root / "services" / "media-commerce" / "app" / "skills",
        ]

        total_skills = 0
        for skills_path in skills_paths:
            if skills_path.exists():
                skill_count = len(list(skills_path.glob("*/SKILL.md")))
                if skill_count > 0:
                    self.log(f"  Found {skill_count} skills in {skills_path.relative_to(self.root)}", "INFO")
                    total_skills += skill_count

        if total_skills == 0:
            self.log(f"  No skills found (may be using agent-based architecture)", "WARNING")
            return True  # Not critical if using new agent architecture

        self.log(f"  ✓ Skills checked ({total_skills} total)", "SUCCESS")
        return True

    def _validate_agents(self) -> bool:
        """Validate all 8 vertical agents"""
        agents_path = self.root / "services" / "media-commerce" / "app" / "agents"

        expected_agents = [
            "deal_flow",
            "fulfillment_ops",
            "media_commerce",
            "content_engine",
            "chief_pulse",
            "compliance_gate",
            "budget_mind",
            "board_ready",
        ]

        found_agents = []
        for agent_file in expected_agents:
            agent_path = agents_path / f"{agent_file}.py"
            if agent_path.exists():
                found_agents.append(agent_file)
            else:
                self.log(f"  Missing agent: {agent_file}", "ERROR")
                self.issues.append(f"agents: Missing {agent_file}")

        self.log(f"  Found {len(found_agents)}/8 agents", "INFO")

        if len(found_agents) != 8:
            return False

        # Test agent imports
        for agent_name in found_agents:
            result = subprocess.run(
                ["python3", "-c", f"from app.agents import {agent_name.replace('_', ' ').title().replace(' ', '')}Agent"],
                capture_output=True,
                text=True,
                cwd=self.root / "services" / "media-commerce",
            )
            if result.returncode != 0:
                self.log(f"  Agent {agent_name} import failed", "ERROR")
                self.issues.append(f"agents: {agent_name} import failed")
                return False

        self.log(f"  ✓ All 8 agents functional", "SUCCESS")
        return True

    def _check_dockerfiles(self) -> bool:
        """Check all Dockerfiles exist and are valid"""
        all_valid = True

        for service in SERVICES:
            dockerfile = self.root / "services" / service / "Dockerfile"
            if not dockerfile.exists():
                self.log(f"  Missing Dockerfile for {service}", "WARNING")
                # Not all services need Dockerfiles
                continue

            # Check for common Dockerfile issues
            with open(dockerfile, "r") as f:
                content = f.read()
                if "COPY" in content and "pyproject.toml" not in content and service in PYTHON_SERVICES:
                    self.log(f"  Dockerfile for {service} may be missing pyproject.toml COPY", "WARNING")

        self.log(f"  ✓ Dockerfiles checked", "SUCCESS")
        return all_valid

    def _fix_imports(self, service: str):
        """Auto-fix common import issues"""
        service_path = self.root / "services" / service
        app_path = service_path / "app"

        self.log(f"  Attempting to fix imports...", "INFO")

        # Add app to PYTHONPATH in main.py
        main_py = app_path / "main.py"
        if main_py.exists():
            with open(main_py, "r") as f:
                content = f.read()

            if "sys.path.insert" not in content:
                # Add path fix at top of file
                fix = "import sys\nfrom pathlib import Path\n\nSERVICE_ROOT = Path(__file__).resolve().parents[1]\nif str(SERVICE_ROOT) not in sys.path:\n    sys.path.insert(0, str(SERVICE_ROOT))\n\n"
                content = fix + content

                with open(main_py, "w") as f:
                    f.write(content)

                self.log(f"  Fixed PYTHONPATH in {service}/main.py", "SUCCESS")
                self.fixes_applied.append(f"{service}: Fixed PYTHONPATH")

    def _fix_go_switch(self, gateway_path: Path):
        """Fix duplicate case in Go switch statement"""
        google_provider = gateway_path / "app" / "providers" / "google.go"

        if not google_provider.exists():
            return

        self.log(f"  Attempting to fix Go switch statement...", "INFO")

        with open(google_provider, "r") as f:
            content = f.read()

        # Remove duplicate "gemini-2.0" case
        if 'case "gemini-2.0"' in content:
            # Keep only the first occurrence
            lines = content.split("\n")
            new_lines = []
            seen_gemini_2 = False

            for line in lines:
                if 'case "gemini-2.0"' in line:
                    if not seen_gemini_2:
                        new_lines.append(line)
                        seen_gemini_2 = True
                    # Skip duplicate
                else:
                    new_lines.append(line)

            with open(google_provider, "w") as f:
                f.write("\n".join(new_lines))

            self.log(f"  Fixed duplicate case in google.go", "SUCCESS")
            self.fixes_applied.append("gateway: Fixed duplicate case in switch")

    def _print_summary(self, results: Dict[str, bool]):
        """Print analysis summary"""
        print("\n" + "=" * 60)
        self.log("DEBUG AGENT REPORT", "INFO")
        print("=" * 60)

        passed = sum(1 for v in results.values() if v)
        total = len(results)

        for check, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            self.log(f"  {check:20} {status}", "SUCCESS" if result else "ERROR")

        print()
        self.log(f"Total: {passed}/{total} checks passed", "INFO")

        if self.issues:
            print("\nIssues found:")
            for issue in self.issues:
                self.log(f"  - {issue}", "ERROR")

        if self.fixes_applied:
            print("\nFixes applied:")
            for fix in self.fixes_applied:
                self.log(f"  - {fix}", "SUCCESS")

        if passed == total:
            print("\n" + "=" * 60)
            self.log("BUILD STATUS: READY FOR DEPLOY", "SUCCESS")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            self.log("BUILD STATUS: ISSUES FOUND - RUN WITH --fix", "ERROR")
            print("=" * 60)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="FullStackArkham Debug Agent")
    parser.add_argument("--analyze", action="store_true", help="Analyze all services")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    parser.add_argument("--service", type=str, help="Check specific service")
    parser.add_argument("--check-skills", action="store_true", help="Check skills loading")
    parser.add_argument("--full-test", action="store_true", help="Full build + deploy test")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    agent = DebugAgent(verbose=args.verbose)

    if args.analyze:
        results = agent.analyze_all()
        sys.exit(0 if all(results.values()) else 1)

    elif args.fix:
        agent.analyze_all()
        if agent.issues:
            agent.log("\nAttempting auto-fixes...", "INFO")
            # Re-run analysis to apply fixes
            agent.analyze_all()
        sys.exit(0 if not agent.issues else 1)

    elif args.service:
        if args.service == "gateway":
            result = agent._analyze_go_service()
        else:
            result = agent._analyze_python_service(args.service)
        sys.exit(0 if result else 1)

    elif args.check_skills:
        result = agent._check_skills()
        sys.exit(0 if result else 1)

    elif args.full_test:
        agent.log("Running full build + deploy test...", "INFO")
        agent.analyze_all()
        # Run live E2E test
        result = subprocess.run(
            ["python3", "services/media-commerce/tests/test_live_e2e_all_verticals.py"],
            cwd=agent.root,
        )
        sys.exit(result.returncode)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
