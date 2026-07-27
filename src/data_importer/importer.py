"""Core data import logic for external repository scanning."""

import json
import os
import subprocess
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import tempfile
import shutil


class DataImporter:
    """Scans and imports social media schedules and materials from external repos."""

    def __init__(self, repo_url: str, branch: str = "main", token: Optional[str] = None):
        """
        Initialize importer for external repository.

        Args:
            repo_url: URL of the external GitHub repository
            branch: Git branch to scan (default: main)
            token: GitHub personal access token (for private repos)
        """
        self.repo_url = repo_url
        self.branch = branch
        self.token = token
        self.temp_dir = None
        self.repo_path = None

    def clone_repo(self) -> bool:
        """
        Clone the external repository to a temporary directory.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="social_media_import_")

            # Build clone URL with token if provided
            clone_url = self.repo_url
            if self.token and "github.com" in clone_url:
                clone_url = clone_url.replace(
                    "https://github.com/",
                    f"https://{self.token}@github.com/",
                )

            # Clone repository
            subprocess.run(
                ["git", "clone", "--branch", self.branch, clone_url, self.temp_dir],
                check=True,
                capture_output=True,
            )

            self.repo_path = self.temp_dir
            return True

        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository: {e}")
            self.cleanup()
            return False
        except Exception as e:
            print(f"Error during clone: {e}")
            self.cleanup()
            return False

    def scan_schedule(self, schedule_path: str = "schedules/content_schedule.json") -> Dict:
        """
        Scan and load content schedule from external repo.

        Args:
            schedule_path: Path to schedule file in the repo

        Returns:
            Schedule data dict
        """
        if not self.repo_path:
            return {}

        full_path = os.path.join(self.repo_path, schedule_path)

        if not os.path.exists(full_path):
            print(f"Schedule file not found: {full_path}")
            return {}

        try:
            with open(full_path, "r") as f:
                schedule = json.load(f)
            return schedule
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in schedule file: {e}")
            return {}

    def scan_materials(self, materials_path: str = "materials/") -> Dict:
        """
        Scan and inventory materials in external repo.

        Args:
            materials_path: Path to materials directory in the repo

        Returns:
            Dict of materials inventory
        """
        if not self.repo_path:
            return {}

        full_path = os.path.join(self.repo_path, materials_path)

        if not os.path.exists(full_path):
            print(f"Materials directory not found: {full_path}")
            return {}

        materials = {
            "directory": materials_path,
            "timestamp": datetime.now().isoformat(),
            "files": [],
            "by_type": {},
        }

        try:
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, full_path)
                    file_ext = os.path.splitext(file)[1].lower()

                    # Track file
                    materials["files"].append(
                        {
                            "path": rel_path,
                            "name": file,
                            "type": file_ext,
                            "size": os.path.getsize(file_path),
                        }
                    )

                    # Track by type
                    if file_ext not in materials["by_type"]:
                        materials["by_type"][file_ext] = []
                    materials["by_type"][file_ext].append(rel_path)

        except Exception as e:
            print(f"Error scanning materials: {e}")

        return materials

    def extract_post_history(self, schedule: Dict) -> List[Dict]:
        """
        Extract post history/template from schedule.

        Args:
            schedule: Content schedule dict

        Returns:
            List of posts with metadata
        """
        posts = []

        if "posts" in schedule:
            posts = schedule.get("posts", [])
        elif "content" in schedule:
            posts = schedule.get("content", [])
        elif "items" in schedule:
            posts = schedule.get("items", [])

        # Normalize post structure
        normalized = []
        for post in posts:
            normalized.append(
                {
                    "id": post.get("id", post.get("title", "unknown")),
                    "title": post.get("title", ""),
                    "content": post.get("content", post.get("body", "")),
                    "platform": post.get("platform", post.get("channel", "multi")),
                    "scheduled_date": post.get("scheduled_date", post.get("date", "")),
                    "status": post.get("status", "planned"),
                    "industry": post.get("industry", ""),
                    "tags": post.get("tags", []),
                    "metadata": post.get("metadata", {}),
                }
            )

        return normalized

    def import_full_schedule(
        self, schedule_path: str = "schedules/content_schedule.json"
    ) -> Tuple[Dict, Dict, List[Dict]]:
        """
        Perform full import: clone, scan schedule, scan materials, extract posts.

        Args:
            schedule_path: Path to schedule file in external repo

        Returns:
            Tuple of (schedule_data, materials_inventory, post_history)
        """
        if not self.clone_repo():
            return {}, {}, []

        try:
            schedule = self.scan_schedule(schedule_path)
            materials = self.scan_materials()
            posts = self.extract_post_history(schedule)

            return schedule, materials, posts

        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"Warning: Failed to cleanup temp directory: {e}")


def import_external_schedule(
    repo_url: str, branch: str = "main", token: Optional[str] = None
) -> Tuple[Dict, Dict, List[Dict]]:
    """
    Convenience function to import schedule from external repo.

    Args:
        repo_url: URL of external repository
        branch: Git branch to use
        token: GitHub token for private repos

    Returns:
        Tuple of (schedule, materials, posts)
    """
    importer = DataImporter(repo_url, branch, token)
    return importer.import_full_schedule()
