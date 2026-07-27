"""Core scheduling and posting logic."""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class Scheduler:
    """Manages scheduled posting of approved content to social platforms."""

    PLATFORMS = ["linkedin", "twitter", "instagram", "facebook", "tiktok", "youtube"]

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize scheduler with configuration.

        Args:
            config: Configuration dict with posting cadence settings
        """
        self.config = config or {}
        self.posting_cadence = config.get("posting_cadence", {})
        self.scheduled_dir = "data/scheduled/"
        self.posted_dir = "data/posted/"
        os.makedirs(self.scheduled_dir, exist_ok=True)
        os.makedirs(self.posted_dir, exist_ok=True)

    def create_schedule_entry(
        self,
        platform: str,
        content: str,
        industry: str,
        scheduled_time: datetime,
        metadata: Optional[Dict] = None,
    ) -> Dict:
        """
        Create a scheduled post entry.

        Args:
            platform: Social platform (linkedin, twitter, etc.)
            content: Post content/message
            industry: Industry this post targets
            scheduled_time: When to post
            metadata: Optional additional metadata

        Returns:
            Schedule entry dict
        """
        entry = {
            "id": f"{platform}_{industry}_{scheduled_time.timestamp()}",
            "platform": platform,
            "content": content,
            "industry": industry,
            "scheduled_time": scheduled_time.isoformat(),
            "created_at": datetime.now().isoformat(),
            "status": "scheduled",
            "metadata": metadata or {},
        }
        return entry

    def queue_posts(
        self, approved_pivots: List[Dict], cadence_config: Optional[Dict] = None
    ) -> Dict:
        """
        Queue approved pivot content for posting per cadence.

        Args:
            approved_pivots: List of approved pivot items
            cadence_config: Posting cadence configuration

        Returns:
            Results dict with queuing summary
        """
        if not cadence_config:
            cadence_config = self.posting_cadence

        results = {
            "total_approved": len(approved_pivots),
            "posts_queued": 0,
            "by_platform": {},
            "queue_files": [],
            "next_post_window": None,
        }

        # For each approved pivot, create posts for each platform
        for pivot in approved_pivots:
            industry_id = pivot.get("industry_id", "unknown")
            industry_name = pivot.get("industry_name", industry_id)

            for platform in self.PLATFORMS:
                platform_config = cadence_config.get(platform, {})

                if not platform_config.get("enabled", True):
                    continue

                # Calculate next posting slot
                next_post_time = self._calculate_next_post_time(platform_config)

                # Create queue entry
                queue_entry = {
                    "platform": platform,
                    "industry": industry_id,
                    "industry_name": industry_name,
                    "scheduled_time": next_post_time.isoformat(),
                    "status": "queued",
                    "created_at": datetime.now().isoformat(),
                }

                # Track by platform
                if platform not in results["by_platform"]:
                    results["by_platform"][platform] = 0
                results["by_platform"][platform] += 1

                results["posts_queued"] += 1

                # Save queue entry
                queue_file = os.path.join(
                    self.scheduled_dir, f"{industry_id}_{platform}_{int(next_post_time.timestamp())}.json"
                )
                with open(queue_file, "w") as f:
                    json.dump(queue_entry, f, indent=2)

                results["queue_files"].append(queue_file)

                # Track earliest post time
                if not results["next_post_window"]:
                    results["next_post_window"] = next_post_time.isoformat()
                else:
                    earliest = datetime.fromisoformat(results["next_post_window"])
                    if next_post_time < earliest:
                        results["next_post_window"] = next_post_time.isoformat()

        return results

    def _calculate_next_post_time(self, platform_config: Dict) -> datetime:
        """
        Calculate the next posting time for a platform based on cadence.

        Args:
            platform_config: Platform cadence configuration

        Returns:
            Next posting datetime
        """
        frequency = platform_config.get("frequency", "daily")
        best_time = platform_config.get("best_time", "09:00")

        # Parse time
        hour, minute = map(int, best_time.split(":"))

        # Create next occurrence
        now = datetime.now()
        next_post = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        # If time has passed today, schedule for tomorrow
        if next_post <= now:
            next_post += timedelta(days=1)

        # Adjust based on frequency
        if frequency == "weekly":
            # Schedule for next week same day
            days_until_next = 7 - now.weekday()
            if days_until_next <= 0:
                days_until_next += 7
            next_post += timedelta(days=days_until_next)

        return next_post

    def get_scheduled_posts(self) -> List[Dict]:
        """
        Get all currently scheduled posts.

        Returns:
            List of scheduled post entries
        """
        posts = []

        if not os.path.exists(self.scheduled_dir):
            return posts

        for filename in os.listdir(self.scheduled_dir):
            if filename.endswith(".json"):
                try:
                    filepath = os.path.join(self.scheduled_dir, filename)
                    with open(filepath, "r") as f:
                        post = json.load(f)

                    if post.get("status") == "queued":
                        posts.append(post)

                except Exception as e:
                    print(f"Error loading scheduled post {filename}: {e}")

        # Sort by scheduled time
        return sorted(posts, key=lambda x: x.get("scheduled_time", ""))

    def mark_posted(self, post_id: str, platform: str) -> bool:
        """
        Mark a post as posted and move to history.

        Args:
            post_id: Post identifier
            platform: Platform it was posted to

        Returns:
            True if successful
        """
        try:
            # Find and update the post file
            for filename in os.listdir(self.scheduled_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(self.scheduled_dir, filename)
                    with open(filepath, "r") as f:
                        post = json.load(f)

                    if post.get("id") == post_id:
                        post["status"] = "posted"
                        post["posted_at"] = datetime.now().isoformat()

                        # Move to posted directory
                        posted_file = os.path.join(
                            self.posted_dir, f"{post_id}_{int(datetime.now().timestamp())}.json"
                        )
                        with open(posted_file, "w") as f:
                            json.dump(post, f, indent=2)

                        # Remove from scheduled
                        os.remove(filepath)
                        return True

            return False

        except Exception as e:
            print(f"Error marking post as posted: {e}")
            return False

    def get_posting_status(self) -> Dict:
        """
        Get overall posting status and statistics.

        Returns:
            Status summary dict
        """
        scheduled = self.get_scheduled_posts()

        # Count posted items
        posted_count = 0
        if os.path.exists(self.posted_dir):
            posted_count = len([f for f in os.listdir(self.posted_dir) if f.endswith(".json")])

        # Group scheduled by platform
        by_platform = {}
        for post in scheduled:
            platform = post.get("platform", "unknown")
            if platform not in by_platform:
                by_platform[platform] = 0
            by_platform[platform] += 1

        return {
            "timestamp": datetime.now().isoformat(),
            "scheduled_count": len(scheduled),
            "posted_count": posted_count,
            "by_platform": by_platform,
            "next_post": scheduled[0] if scheduled else None,
        }
