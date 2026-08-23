"""Content library and file management"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import shutil


class ContentManager:
    """Manages content library - uploads, organizes, and tracks marketing materials"""

    ALLOWED_TYPES = {
        "video": [".mp4", ".mov", ".avi", ".webm", ".mkv"],
        "image": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
        "document": [".pdf", ".docx", ".txt", ".md"],
        "template": [".pptx", ".xlsx", ".html"],
    }

    def __init__(self, library_dir: str = None):
        """Initialize content manager"""
        if library_dir is None:
            # Use portable location relative to app
            library_dir = os.path.join(os.getcwd(), "data", "content_library")
        self.library_dir = library_dir
        self.metadata_file = os.path.join(library_dir, "library_manifest.json")
        os.makedirs(library_dir, exist_ok=True)
        self._load_manifest()

    def _load_manifest(self) -> None:
        """Load or create library manifest"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r") as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {"items": [], "categories": {}}
            self._save_manifest()

    def _save_manifest(self) -> None:
        """Save manifest to file"""
        with open(self.metadata_file, "w") as f:
            json.dump(self.manifest, f, indent=2)

    def upload_material(
        self,
        file_path: str,
        title: str,
        category: str,
        industry: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
    ) -> Dict:
        """
        Add material to library.

        Args:
            file_path: Path to the file
            title: Display name
            category: Type (video, image, document, template)
            industry: Which industry this is for
            description: What it's about
            tags: Search tags

        Returns:
            Item metadata dict
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": "File not found"}

        # Validate file type
        ext = os.path.splitext(file_path)[1].lower()
        if not any(ext in exts for exts in self.ALLOWED_TYPES.values()):
            return {"success": False, "error": f"File type {ext} not allowed"}

        # Copy file to library
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(self.library_dir, file_name)

        try:
            shutil.copy2(file_path, dest_path)
        except Exception as e:
            return {"success": False, "error": str(e)}

        # Create metadata
        item = {
            "id": f"{int(datetime.now().timestamp())}",
            "filename": file_name,
            "title": title,
            "category": category,
            "industry": industry,
            "description": description,
            "tags": tags or [],
            "uploaded_at": datetime.now().isoformat(),
            "file_size": os.path.getsize(dest_path),
        }

        # Add to manifest
        self.manifest["items"].append(item)
        if category not in self.manifest["categories"]:
            self.manifest["categories"][category] = []
        self.manifest["categories"][category].append(item["id"])

        self._save_manifest()

        return {"success": True, "item": item}

    def get_library(
        self, category: Optional[str] = None, industry: Optional[str] = None
    ) -> List[Dict]:
        """
        Get library contents with optional filtering.

        Args:
            category: Filter by type (video, image, etc)
            industry: Filter by industry

        Returns:
            List of items
        """
        items = self.manifest.get("items", [])

        if category:
            items = [i for i in items if i["category"] == category]

        if industry:
            items = [i for i in items if i["industry"] == industry]

        return sorted(items, key=lambda x: x["uploaded_at"], reverse=True)

    def get_item(self, item_id: str) -> Optional[Dict]:
        """Get specific item metadata"""
        for item in self.manifest.get("items", []):
            if item["id"] == item_id:
                return item
        return None

    def delete_material(self, item_id: str) -> bool:
        """Delete material from library"""
        item = self.get_item(item_id)
        if not item:
            return False

        # Delete file
        file_path = os.path.join(self.library_dir, item["filename"])
        if os.path.exists(file_path):
            os.remove(file_path)

        # Remove from manifest
        self.manifest["items"] = [i for i in self.manifest["items"] if i["id"] != item_id]

        # Remove from categories
        category = item["category"]
        if category in self.manifest["categories"]:
            self.manifest["categories"][category] = [
                id for id in self.manifest["categories"][category] if id != item_id
            ]

        self._save_manifest()
        return True

    def search_library(self, query: str) -> List[Dict]:
        """Search library by title, description, tags"""
        results = []
        query_lower = query.lower()

        for item in self.manifest.get("items", []):
            if (
                query_lower in item["title"].lower()
                or query_lower in item["description"].lower()
                or any(query_lower in tag.lower() for tag in item.get("tags", []))
            ):
                results.append(item)

        return results

    def get_stats(self) -> Dict:
        """Get library statistics"""
        items = self.manifest.get("items", [])
        categories = self.manifest.get("categories", {})

        stats = {
            "total_items": len(items),
            "by_category": {},
            "total_size_mb": 0,
            "industries": set(),
        }

        for category, ids in categories.items():
            stats["by_category"][category] = len(ids)

        for item in items:
            stats["total_size_mb"] += item.get("file_size", 0) / (1024 * 1024)
            if item.get("industry"):
                stats["industries"].add(item["industry"])

        stats["industries"] = list(stats["industries"])
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)

        return stats
