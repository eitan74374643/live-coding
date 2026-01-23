"""
DavidAI - Multi-Agent Coding Ecosystem

Usage:
    python main.py
"""

from davidai.core.orchestrator import DavidAI

if __name__ == "__main__":
    print("Initializing DavidAI Multi-Agent Ecosystem...")
    davidai = DavidAI()
    try:
        davidai.run_interactive()
    except KeyboardInterrupt:
        davidai.shutdown()

