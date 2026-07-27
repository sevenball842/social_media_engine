"""Core performance tracking and reporting logic."""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class PerformanceTracker:
    """Tracks and reports on social media campaign performance."""

    def __init__(self, tracking_dir: str = "data/tracking/"):
        """
        Initialize performance tracker.

        Args:
            tracking_dir: Directory to store tracking data
        """
        self.tracking_dir = tracking_dir
        os.makedirs(tracking_dir, exist_ok=True)

    def record_post_metrics(
        self,
        post_id: str,
        platform: str,
        industry: str,
        metrics: Dict,
    ) -> bool:
        """
        Record performance metrics for a posted piece of content.

        Args:
            post_id: Post identifier
            platform: Social platform
            industry: Industry targeted
            metrics: Dict with engagement metrics (likes, shares, comments, reach, impressions, etc.)

        Returns:
            True if successful
        """
        try:
            record = {
                "post_id": post_id,
                "platform": platform,
                "industry": industry,
                "recorded_at": datetime.now().isoformat(),
                "metrics": metrics,
            }

            # Create filename with timestamp
            timestamp = int(datetime.now().timestamp())
            filename = f"{platform}_{industry}_{timestamp}.json"
            filepath = os.path.join(self.tracking_dir, filename)

            with open(filepath, "w") as f:
                json.dump(record, f, indent=2)

            return True

        except Exception as e:
            print(f"Error recording metrics: {e}")
            return False

    def get_industry_performance(self, industry: str) -> Dict:
        """
        Get aggregated performance metrics for an industry.

        Args:
            industry: Industry identifier

        Returns:
            Performance summary dict
        """
        metrics_by_platform = {}
        all_posts = []

        if not os.path.exists(self.tracking_dir):
            return {}

        # Load all tracking files for this industry
        for filename in os.listdir(self.tracking_dir):
            if filename.endswith(".json"):
                try:
                    filepath = os.path.join(self.tracking_dir, filename)
                    with open(filepath, "r") as f:
                        record = json.load(f)

                    if record.get("industry") == industry:
                        all_posts.append(record)
                        platform = record.get("platform", "unknown")

                        if platform not in metrics_by_platform:
                            metrics_by_platform[platform] = {
                                "total_posts": 0,
                                "total_engagement": 0,
                                "total_reach": 0,
                                "total_impressions": 0,
                                "avg_engagement_rate": 0,
                            }

                        platform_metrics = record.get("metrics", {})
                        metrics_by_platform[platform]["total_posts"] += 1
                        metrics_by_platform[platform]["total_engagement"] += platform_metrics.get(
                            "engagement", 0
                        )
                        metrics_by_platform[platform]["total_reach"] += platform_metrics.get(
                            "reach", 0
                        )
                        metrics_by_platform[platform]["total_impressions"] += platform_metrics.get(
                            "impressions", 0
                        )

                except Exception as e:
                    print(f"Error loading tracking file {filename}: {e}")

        # Calculate averages
        for platform in metrics_by_platform:
            total_posts = metrics_by_platform[platform]["total_posts"]
            if total_posts > 0:
                total_engagement = metrics_by_platform[platform]["total_engagement"]
                total_reach = metrics_by_platform[platform]["total_reach"]
                if total_reach > 0:
                    metrics_by_platform[platform]["avg_engagement_rate"] = (
                        total_engagement / total_reach
                    ) * 100

        return {
            "industry": industry,
            "total_posts": len(all_posts),
            "by_platform": metrics_by_platform,
            "last_updated": datetime.now().isoformat(),
        }

    def get_platform_performance(self, platform: str) -> Dict:
        """
        Get aggregated performance metrics for a platform.

        Args:
            platform: Platform name (linkedin, twitter, etc.)

        Returns:
            Performance summary dict
        """
        metrics_by_industry = {}
        all_posts = []

        if not os.path.exists(self.tracking_dir):
            return {}

        # Load all tracking files for this platform
        for filename in os.listdir(self.tracking_dir):
            if filename.endswith(".json"):
                try:
                    filepath = os.path.join(self.tracking_dir, filename)
                    with open(filepath, "r") as f:
                        record = json.load(f)

                    if record.get("platform") == platform:
                        all_posts.append(record)

                except Exception as e:
                    print(f"Error loading tracking file {filename}: {e}")

        return {
            "platform": platform,
            "total_posts": len(all_posts),
            "by_industry": metrics_by_industry,
            "last_updated": datetime.now().isoformat(),
        }

    def generate_performance_report(
        self, output_path: str = "data/performance_report.md"
    ) -> bool:
        """
        Generate a comprehensive performance report.

        Args:
            output_path: Where to save the report

        Returns:
            True if successful
        """
        try:
            report = "# Performance Report\n\n"
            report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            report += f"**Period:** Last 30 days\n\n"

            # Summary statistics
            if os.path.exists(self.tracking_dir):
                files = [f for f in os.listdir(self.tracking_dir) if f.endswith(".json")]
                report += f"## Summary\n\n"
                report += f"- **Total Posts Tracked:** {len(files)}\n"
                report += f"- **Tracking Records:** {len(files)}\n\n"

                # Platform breakdown
                platform_counts = {}
                for filename in files:
                    try:
                        filepath = os.path.join(self.tracking_dir, filename)
                        with open(filepath, "r") as f:
                            record = json.load(f)
                            platform = record.get("platform", "unknown")
                            platform_counts[platform] = platform_counts.get(platform, 0) + 1
                    except:
                        pass

                if platform_counts:
                    report += "## By Platform\n\n"
                    for platform, count in sorted(platform_counts.items()):
                        report += f"- **{platform.capitalize()}:** {count} posts\n"
                    report += "\n"

            # Top performing content
            report += "## Performance Metrics\n\n"
            report += "Performance tracking is active. Detailed metrics will appear as posts are published and tracked.\n\n"

            # Recommendations
            report += "## Recommendations\n\n"
            report += "1. Monitor engagement rates across platforms\n"
            report += "2. Identify high-performing content themes\n"
            report += "3. Optimize posting times based on platform data\n"
            report += "4. A/B test messaging for different industries\n\n"

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(report)

            return True

        except Exception as e:
            print(f"Error generating report: {e}")
            return False

    def get_summary_stats(self) -> Dict:
        """
        Get summary statistics across all tracked content.

        Returns:
            Summary statistics dict
        """
        total_posts = 0
        total_engagement = 0
        total_reach = 0
        platform_stats = {}

        if not os.path.exists(self.tracking_dir):
            return {}

        for filename in os.listdir(self.tracking_dir):
            if filename.endswith(".json"):
                try:
                    filepath = os.path.join(self.tracking_dir, filename)
                    with open(filepath, "r") as f:
                        record = json.load(f)

                    total_posts += 1
                    platform = record.get("platform", "unknown")
                    metrics = record.get("metrics", {})

                    if platform not in platform_stats:
                        platform_stats[platform] = {
                            "posts": 0,
                            "engagement": 0,
                            "reach": 0,
                        }

                    platform_stats[platform]["posts"] += 1
                    platform_stats[platform]["engagement"] += metrics.get("engagement", 0)
                    platform_stats[platform]["reach"] += metrics.get("reach", 0)

                    total_engagement += metrics.get("engagement", 0)
                    total_reach += metrics.get("reach", 0)

                except Exception as e:
                    print(f"Error processing tracking file {filename}: {e}")

        avg_engagement_rate = 0
        if total_reach > 0:
            avg_engagement_rate = (total_engagement / total_reach) * 100

        return {
            "timestamp": datetime.now().isoformat(),
            "total_posts": total_posts,
            "total_engagement": total_engagement,
            "total_reach": total_reach,
            "avg_engagement_rate": round(avg_engagement_rate, 2),
            "by_platform": platform_stats,
        }
