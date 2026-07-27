"""Core content generation logic."""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class ContentGenerator:
    """Generates campaign pivot MD files for industries with status changes."""

    def __init__(self, template_path: Optional[str] = None):
        """
        Initialize generator with campaign pivot template.

        Args:
            template_path: Path to campaign_pivot.md template file
        """
        self.template_path = template_path or "templates/campaign_pivot.md"
        self.template_content = self._load_template()

    def _load_template(self) -> str:
        """Load the campaign pivot template."""
        if not os.path.exists(self.template_path):
            return ""

        with open(self.template_path, "r") as f:
            return f.read()

    def generate_pivot_file(
        self, industry_data: Dict, status_change: Dict, output_path: str
    ) -> bool:
        """
        Generate a campaign pivot MD file for an industry with status change.

        Args:
            industry_data: Industry data dict from status calculation
            status_change: Status change data from StatusCalculator
            output_path: Where to save the generated MD file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare substitutions
            substitutions = {
                "[INDUSTRY_NAME]": status_change.get("industry_name", "Unknown"),
                "[DATE]": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "[PREVIOUS]": status_change.get("previous_status", "UNKNOWN"),
                "[CURRENT]": status_change.get("new_status", "UNKNOWN"),
                "[PERCENT_CHANGE]": str(status_change.get("percent_change", 0)),
                "[INDUSTRY]": status_change.get("industry_id", "unknown"),
                "[HIGH/MEDIUM/LOW]": self._determine_priority(
                    status_change.get("new_status", "GREEN")
                ),
            }

            # Generate content from template
            content = self.template_content
            for placeholder, value in substitutions.items():
                content = content.replace(placeholder, str(value))

            # Add industry-specific insights
            content = self._add_insights(content, industry_data, status_change)

            # Write file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"Error generating pivot file: {e}")
            return False

    def _determine_priority(self, status: str) -> str:
        """Determine priority level based on status."""
        priority_map = {
            "RED": "HIGH",
            "ORANGE": "HIGH",
            "YELLOW": "MEDIUM",
            "GREEN": "LOW",
        }
        return priority_map.get(status, "MEDIUM")

    def _add_insights(
        self, content: str, industry_data: Dict, status_change: Dict
    ) -> str:
        """Add industry-specific insights to generated content."""
        # Add specific insights based on industry and status
        insights_section = f"\n\n## Industry Context\n\n"
        insights_section += f"- **Units Sold This Quarter:** {industry_data.get('units_sold', 'N/A')}\n"
        insights_section += f"- **Primary Product:** {industry_data.get('primary_product', 'Web Scanning Tool')}\n"
        insights_section += f"- **Notes:** {industry_data.get('notes', 'No additional notes')}\n"

        # Insert before approval section if it exists
        if "### For Tim's Review:" in content:
            content = content.replace(
                "### For Tim's Review:",
                insights_section + "\n### For Tim's Review:",
            )
        else:
            # Add at end before archive section
            if "## Archive" in content:
                content = content.replace("## Archive", insights_section + "\n## Archive")
            else:
                content += insights_section

        return content

    def generate_batch_pivots(
        self, status_changes: List[Dict], output_dir: str = "data/approval_queue/"
    ) -> Dict:
        """
        Generate pivot files for all industries with status changes.

        Args:
            status_changes: List of status changes from StatusCalculator
            output_dir: Directory to save generated files

        Returns:
            Summary dict with generation results
        """
        results = {
            "total_requested": len(status_changes),
            "successful": 0,
            "failed": 0,
            "files_created": [],
            "errors": [],
        }

        for status_change in status_changes:
            industry_id = status_change.get("industry_id", "unknown")
            industry_name = status_change.get("industry_name", industry_id)

            # Create filename
            filename = (
                f"{industry_id}_pivot_{datetime.now().strftime('%Y%m%d')}.md"
            )
            filepath = os.path.join(output_dir, filename)

            # Generate file
            if self.generate_pivot_file(status_change, status_change, filepath):
                results["successful"] += 1
                results["files_created"].append(
                    {
                        "filename": filename,
                        "industry": industry_name,
                        "status": status_change.get("new_status"),
                        "path": filepath,
                    }
                )
            else:
                results["failed"] += 1
                results["errors"].append(f"Failed to generate pivot for {industry_name}")

        return results

    def create_summary_index(
        self, status_changes: List[Dict], output_path: str = "data/approval_queue/INDEX.md"
    ) -> bool:
        """
        Create an index of all generated pivot files.

        Args:
            status_changes: List of status changes
            output_path: Where to save the index

        Returns:
            True if successful, False otherwise
        """
        try:
            index_content = "# Approval Queue Index\n\n"
            index_content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            index_content += f"**Status Changes Requiring Review:** {len(status_changes)}\n\n"

            # Group by status for easy navigation
            by_status = {}
            for change in status_changes:
                status = change.get("new_status", "UNKNOWN")
                if status not in by_status:
                    by_status[status] = []
                by_status[status].append(change)

            # Create summary table
            index_content += "## Summary Table\n\n"
            index_content += "| Industry | Previous | New | Change | Priority |\n"
            index_content += "|----------|----------|-----|--------|----------|\n"

            for status in ["RED", "ORANGE", "YELLOW", "GREEN"]:
                for change in by_status.get(status, []):
                    priority = self._determine_priority(status)
                    index_content += (
                        f"| {change.get('industry_name')} | "
                        f"{change.get('previous_status')} | "
                        f"{status} | "
                        f"{change.get('percent_change')}% | "
                        f"{priority} |\n"
                    )

            index_content += "\n## Files to Review\n\n"
            for status in ["RED", "ORANGE", "YELLOW", "GREEN"]:
                if by_status.get(status):
                    index_content += f"\n### {status} Status Changes\n\n"
                    for change in by_status[status]:
                        industry_id = change.get("industry_id", "unknown")
                        filename = (
                            f"{industry_id}_pivot_{datetime.now().strftime('%Y%m%d')}.md"
                        )
                        index_content += f"- [{change.get('industry_name')}](./{filename})\n"

            # Write index
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(index_content)

            return True

        except Exception as e:
            print(f"Error creating summary index: {e}")
            return False
