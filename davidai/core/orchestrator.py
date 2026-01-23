"""
DavidAI Orchestrator.
Central control unit managing the lifecycle of the multi-agent ecosystem.
"""

import time
import logging
import threading
import json
from typing import Dict, Any, List, Optional
from .loader import DavidAIModelManager
from .agents import CEO, Manager, ANT, KnowledgeCurator
from ..utils.file_utils import PathGuard, ProjectStructure
from ..ui.command_center import Dashboard, CommandInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DavidAI:
    """
    Main class for the DavidAI Ecosystem.
    Integrates all components and manages the workflow.
    """

    def __init__(self, workspace_root: str = "/home/engine/project"):
        self.workspace_root = workspace_root
        self.is_running = False
        self.is_paused = False

        # Initialize Core Components
        logger.info("Initializing DavidAI components...")
        self.model_manager = DavidAIModelManager()
        self.path_guard = PathGuard(workspace_root)
        self.project_structure = ProjectStructure(workspace_root, self.path_guard)

        # Initialize Agents
        self.model_manager.load_all()
        self.ceo = CEO(self.model_manager)
        self.manager = Manager(self.model_manager)
        self.knowledge_curator = KnowledgeCurator()

        # Setup ANTS
        self.ants = []
        ant_roles = [
            (1, "Boilerplate"),
            (2, "LogicStubs"),
            (3, "DebugPatch"),
            (4, "AutoTest"),
            (5, "Docs"),
            (6, "DeepLogic")
        ]
        for role_id, name in ant_roles:
            ant = ANT(role_id, name, self.model_manager)
            self.ants.append(ant)
        self.manager.register_ants(self.ants)

        # UI
        self.dashboard = Dashboard()
        self.interface = CommandInterface(self.dashboard, self)

        logger.info("DavidAI initialized successfully.")

    def start_cycle(self):
        """
        Start the autonomous 12-hour cycle.
        """
        if self.is_running:
            return

        self.is_running = True
        self.dashboard.log_message("SYSTEM", "Starting autonomous cycle...")

        # Start the dashboard in a separate thread
        self.dashboard_thread = threading.Thread(target=self.dashboard.start)
        self.dashboard_thread.start()

        # Main loop (simulated)
        self.main_loop_thread = threading.Thread(target=self._run_cycle)
        self.main_loop_thread.start()

    def pause_cycle(self):
        """
        Pause the current cycle.
        """
        self.is_paused = not self.is_paused
        status = "Paused" if self.is_paused else "Resumed"
        self.dashboard.log_message("SYSTEM", f"Cycle {status}.")
        self.dashboard.is_running = not self.is_paused

    def _run_cycle(self):
        """
        Internal method running the recursive loop.
        """
        start_time = time.time()
        cycle_duration = 12 * 60 * 60  # 12 hours

        while self.is_running:
            if self.is_paused:
                time.sleep(1)
                continue

            if time.time() - start_time > cycle_duration:
                self.dashboard.log_message("SYSTEM", "Cycle complete.")
                self.shutdown()
                return

            # Simulate Work Cycle
            self._simulate_work()

            # Sleep briefly to prevent CPU hogging in this simulation
            time.sleep(5)

    def _simulate_work(self):
        """
        Simulates a cycle of work (Plan -> Generate -> Verify -> Consolidate).
        """
        self.dashboard.update_metrics({"active_agents": 6, "tasks_completed": 10})

        # 1. Plan
        plan = self.ceo.run({"type": "plan", "description": "New coding task"})
        self.dashboard.log_message("CEO", "Architecture planned.")

        # 2. Generate
        task = {"type": "assign_task", "description": "Implement feature X"}
        results = self.manager.run(task)
        self.dashboard.log_message("Manager", "Tasks assigned to ANTS.")

        # 3. Verify & Heal (Mock)
        # 4. Consolidate
        self.knowledge_curator.log_success({"task": "simulated_task", "success": True})

    def get_status(self) -> Dict[str, Any]:
        return {
            "running": self.is_running,
            "paused": self.is_paused,
            "agents_active": sum(1 for ant in self.ants if ant.is_active),
            "knowledge_base_size": len(self.knowledge_curator.get_consolidated_knowledge())
        }

    def get_project_tree(self) -> List[str]:
        return self.project_structure.get_tree()

    def shutdown(self):
        self.is_running = False
        self.dashboard.stop()
        logger.info("DavidAI shutting down.")

    def run_interactive(self):
        """
        Start the interactive command interface.
        """
        self.interface.run()


# Main Entry Point
if __name__ == "__main__":
    davidai = DavidAI()
    try:
        davidai.run_interactive()
    except KeyboardInterrupt:
        davidai.shutdown()

