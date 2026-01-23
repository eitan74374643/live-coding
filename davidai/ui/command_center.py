"""
DavidAI Command Center (Terminal UI).
A Text-based User Interface (TUI) for managing the DavidAI ecosystem.
Provides visualization of the project tree, agent status, and control mechanisms.
"""

import sys
import time
import threading
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Note: In a full installation, we would use 'textual'. For this environment, we simulate the UI structure.
# If 'textual' or 'curses' isn't available, we fall back to a simple logger-based dashboard.

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DavidAI-UI")


class Dashboard:
    """
    Simple dashboard to print status updates to the console.
    In a full implementation, this would be a Textual App.
    """

    def __init__(self):
        self.is_running = False
        self.metrics = {
            "gpu_vram": "0 / 12 GB",
            "cpu_load": "0%",
            "active_agents": 0,
            "tasks_completed": 0,
            "errors": 0
        }
        self.logs: List[str] = []

    def log_message(self, source: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{source}] {message}"
        self.logs.append(formatted)
        if len(self.logs) > 50:
            self.logs.pop(0)
        print(formatted)

    def update_metrics(self, new_metrics: Dict[str, Any]):
        self.metrics.update(new_metrics)

    def render(self):
        if not self.is_running:
            return

        # Clear screen (simplified for cross-platform)
        print("\033[H", end="")

        print("=" * 60)
        print(f" DAVIDAI COMMAND CENTER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ")
        print("=" * 60)
        print(f" [SYSTEM STATUS] {'RUNNING' if self.is_running else 'PAUSED'}")
        print("-" * 60)
        print(f" [METRICS]")
        print(f"  GPU VRAM: {self.metrics.get('gpu_vram', 'N/A')}")
        print(f"  CPU Load: {self.metrics.get('cpu_load', 'N/A')}")
        print(f"  Active Agents: {self.metrics.get('active_agents', 0)}")
        print(f"  Tasks Completed: {self.metrics.get('tasks_completed', 0)}")
        print(f"  Errors: {self.metrics.get('errors', 0)}")
        print("-" * 60)
        print(f" [RECENT LOGS]")
        for log in self.logs[-10:]:
            print(f"  {log}")
        print("=" * 60)

    def start(self):
        self.is_running = True
        logger.info("Dashboard started.")
        self.render_loop()

    def stop(self):
        self.is_running = False
        logger.info("Dashboard stopped.")

    def render_loop(self):
        while self.is_running:
            self.render()
            time.sleep(2)


class CommandInterface:
    """
    Interactive shell for the user to control DavidAI.
    """

    def __init__(self, dashboard: Dashboard, ecosystem_ref):
        self.dashboard = dashboard
        self.ecosystem = ecosystem_ref
        self.command_map = {
            "start": self.cmd_start,
            "pause": self.cmd_pause,
            "status": self.cmd_status,
            "inspect": self.cmd_inspect,
            "exit": self.cmd_exit,
            "help": self.cmd_help
        }

    def cmd_start(self, args):
        self.ecosystem.start_cycle()
        self.dashboard.log_message("USER", "System started.")

    def cmd_pause(self, args):
        self.ecosystem.pause_cycle()
        self.dashboard.log_message("USER", "System paused.")

    def cmd_status(self, args):
        status = self.ecosystem.get_status()
        self.dashboard.log_message("SYSTEM", f"Status: {status}")

    def cmd_inspect(self, args):
        self.dashboard.log_message("SYSTEM", "Inspecting project structure...")
        tree = self.ecosystem.get_project_tree()
        for line in tree:
            print(line)

    def cmd_exit(self, args):
        self.ecosystem.shutdown()
        sys.exit(0)

    def cmd_help(self, args):
        help_text = """
        Available Commands:
          start     - Start the autonomous generation cycle
          pause     - Pause the current cycle
          status    - Show system status and metrics
          inspect   - Show project file tree
          exit      - Shutdown and exit
          help      - Show this help message
        """
        print(help_text)

    def run(self):
        print("DavidAI Command Interface Ready. Type 'help' for commands.")
        while True:
            try:
                cmd_input = input("DavidAI > ").strip().split()
                if not cmd_input:
                    continue
                cmd = cmd_input[0].lower()
                args = cmd_input[1:]
                if cmd in self.command_map:
                    self.command_map[cmd](args)
                else:
                    print(f"Unknown command: {cmd}")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                self.cmd_exit([])
                break

