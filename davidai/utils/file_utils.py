"""
File Operations and Security Utilities.
Implements PATH-GUARD and file management for the DavidAI ecosystem.
"""

import os
import json
import logging
import hashlib
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PathGuard:
    """
    Validates file paths to prevent directory traversal attacks.
    Ensures operations stay within the allowed workspace.
    """

    def __init__(self, allowed_root: str):
        self.allowed_root = os.path.abspath(allowed_root)
        logger.info(f"PathGuard initialized. Allowed root: {self.allowed_root}")

    def is_safe_path(self, path: str) -> bool:
        """
        Check if the path is safe (no '..', external drives, etc.).
        """
        abs_path = os.path.abspath(path)
        if abs_path.startswith(self.allowed_root):
            return True
        logger.warning(f"PathGuard blocked access to: {abs_path}")
        return False

    def safe_read(self, path: str) -> Optional[str]:
        if self.is_safe_path(path):
            try:
                with open(path, 'r') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading file {path}: {e}")
        return None

    def safe_write(self, path: str, content: str) -> bool:
        if self.is_safe_path(path):
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write(content)
                return True
            except Exception as e:
                logger.error(f"Error writing file {path}: {e}")
        return False


class ProjectStructure:
    """
    Manages the project structure and file map.
    """

    def __init__(self, root_path: str, path_guard: PathGuard):
        self.root_path = root_path
        self.path_guard = path_guard
        self.file_map: Dict[str, str] = {}

    def scan_directory(self) -> Dict[str, str]:
        """
        Recursively scan directory and build a file map.
        Returns a dictionary of file paths.
        """
        file_map = {}
        for root, dirs, files in os.walk(self.root_path):
            # Skip hidden directories like .git, node_modules
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.root_path)
                if self.path_guard.is_safe_path(full_path):
                    file_map[rel_path] = full_path

        self.file_map = file_map
        return file_map

    def get_tree(self, prefix: str = "") -> List[str]:
        """
        Generate a visual tree structure.
        """
        lines = []
        if not self.file_map:
            self.scan_directory()

        sorted_files = sorted(self.file_map.keys())
        for path in sorted_files:
            lines.append(f"{prefix}{path}")
        return lines

