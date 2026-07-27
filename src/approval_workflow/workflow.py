"""Core approval workflow logic."""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class ApprovalWorkflow:
    """Manages Tim's approval workflow for campaign pivots."""

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_REVISING = "revising"

    def __init__(self, queue_dir: str = "data/approval_queue/"):
        """
        Initialize approval workflow.

        Args:
            queue_dir: Directory where pivot files are stored
        """
        self.queue_dir = queue_dir
        self.metadata_dir = os.path.join(queue_dir, ".metadata")
        os.makedirs(self.metadata_dir, exist_ok=True)

    def create_pending_item(
        self, filename: str, industry_id: str, status_change: Dict
    ) -> bool:
        """
        Create a new pending approval item.

        Args:
            filename: Name of the pivot MD file
            industry_id: Industry identifier
            status_change: Status change data

        Returns:
            True if successful
        """
        try:
            metadata = {
                "filename": filename,
                "industry_id": industry_id,
                "industry_name": status_change.get("industry_name"),
                "status": self.STATUS_PENDING,
                "created_at": datetime.now().isoformat(),
                "expires_at": (
                    datetime.now() + timedelta(days=7)
                ).isoformat(),  # Auto-expire after 7 days
                "previous_status": status_change.get("previous_status"),
                "new_status": status_change.get("new_status"),
                "percent_change": status_change.get("percent_change"),
                "approver_notes": "",
                "approved_at": None,
                "approval_notes": "",
            }

            metadata_path = os.path.join(
                self.metadata_dir, f"{industry_id}.json"
            )
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            return True

        except Exception as e:
            print(f"Error creating pending item: {e}")
            return False

    def get_pending_items(self) -> List[Dict]:
        """
        Get all pending approval items.

        Returns:
            List of pending items
        """
        pending = []

        if not os.path.exists(self.metadata_dir):
            return pending

        for filename in os.listdir(self.metadata_dir):
            if filename.endswith(".json"):
                try:
                    filepath = os.path.join(self.metadata_dir, filename)
                    with open(filepath, "r") as f:
                        metadata = json.load(f)

                    if metadata.get("status") == self.STATUS_PENDING:
                        # Check if expired
                        expires_at = datetime.fromisoformat(
                            metadata.get("expires_at", "")
                        )
                        if datetime.now() > expires_at:
                            metadata["status"] = "expired"
                            self._save_metadata(metadata)
                        else:
                            pending.append(metadata)

                except Exception as e:
                    print(f"Error loading pending item {filename}: {e}")

        return sorted(pending, key=lambda x: x.get("created_at", ""), reverse=True)

    def approve_pivot(
        self, industry_id: str, approval_notes: str = ""
    ) -> bool:
        """
        Mark a pivot as approved by Tim.

        Args:
            industry_id: Industry identifier
            approval_notes: Optional notes from Tim

        Returns:
            True if successful
        """
        try:
            metadata_path = os.path.join(self.metadata_dir, f"{industry_id}.json")

            if not os.path.exists(metadata_path):
                return False

            with open(metadata_path, "r") as f:
                metadata = json.load(f)

            metadata["status"] = self.STATUS_APPROVED
            metadata["approved_at"] = datetime.now().isoformat()
            metadata["approval_notes"] = approval_notes

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            return True

        except Exception as e:
            print(f"Error approving pivot: {e}")
            return False

    def reject_pivot(self, industry_id: str, reason: str = "") -> bool:
        """
        Mark a pivot as rejected, requiring revision.

        Args:
            industry_id: Industry identifier
            reason: Reason for rejection

        Returns:
            True if successful
        """
        try:
            metadata_path = os.path.join(self.metadata_dir, f"{industry_id}.json")

            if not os.path.exists(metadata_path):
                return False

            with open(metadata_path, "r") as f:
                metadata = json.load(f)

            metadata["status"] = self.STATUS_REVISING
            metadata["rejection_reason"] = reason
            metadata["rejected_at"] = datetime.now().isoformat()

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            return True

        except Exception as e:
            print(f"Error rejecting pivot: {e}")
            return False

    def get_approved_pivots(self) -> List[Dict]:
        """Get all approved pivots ready for scheduling."""
        approved = []

        if not os.path.exists(self.metadata_dir):
            return approved

        for filename in os.listdir(self.metadata_dir):
            if filename.endswith(".json"):
                try:
                    filepath = os.path.join(self.metadata_dir, filename)
                    with open(filepath, "r") as f:
                        metadata = json.load(f)

                    if metadata.get("status") == self.STATUS_APPROVED:
                        approved.append(metadata)

                except Exception as e:
                    print(f"Error loading approved item {filename}: {e}")

        return approved

    def get_workflow_status(self) -> Dict:
        """
        Get overall workflow status summary.

        Returns:
            Status summary dict
        """
        status_counts = {
            "pending": 0,
            "approved": 0,
            "rejected": 0,
            "expired": 0,
        }

        all_items = []

        if os.path.exists(self.metadata_dir):
            for filename in os.listdir(self.metadata_dir):
                if filename.endswith(".json"):
                    try:
                        filepath = os.path.join(self.metadata_dir, filename)
                        with open(filepath, "r") as f:
                            metadata = json.load(f)
                            all_items.append(metadata)

                            status = metadata.get("status", "unknown")
                            if status in status_counts:
                                status_counts[status] += 1

                    except Exception as e:
                        print(f"Error loading status for {filename}: {e}")

        return {
            "timestamp": datetime.now().isoformat(),
            "total_items": len(all_items),
            "status_summary": status_counts,
            "items": all_items,
        }

    def _save_metadata(self, metadata: Dict):
        """Save metadata dict to file."""
        try:
            industry_id = metadata.get("industry_id", "unknown")
            metadata_path = os.path.join(self.metadata_dir, f"{industry_id}.json")

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

        except Exception as e:
            print(f"Error saving metadata: {e}")

    def create_approval_report(self, output_path: str = "data/approval_status.md") -> bool:
        """
        Create a summary report of all pending approvals.

        Args:
            output_path: Where to save the report

        Returns:
            True if successful
        """
        try:
            status = self.get_workflow_status()
            pending = self.get_pending_items()

            report = "# Approval Workflow Status\n\n"
            report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

            # Summary
            report += "## Summary\n\n"
            report += f"- **Pending Review:** {status['status_summary'].get('pending', 0)}\n"
            report += f"- **Approved:** {status['status_summary'].get('approved', 0)}\n"
            report += f"- **Rejected (Revising):** {status['status_summary'].get('rejected', 0)}\n"
            report += f"- **Expired:** {status['status_summary'].get('expired', 0)}\n\n"

            # Pending items
            if pending:
                report += "## Pending Review (Action Required)\n\n"
                report += "| Industry | Status Change | File | Priority | Created |\n"
                report += "|----------|---------------|------|----------|----------|\n"

                for item in pending:
                    priority = (
                        "🔴 HIGH"
                        if item.get("new_status") in ["RED", "ORANGE"]
                        else "🟡 MEDIUM"
                        if item.get("new_status") == "YELLOW"
                        else "🟢 LOW"
                    )
                    created = datetime.fromisoformat(
                        item.get("created_at", "")
                    ).strftime("%m-%d %H:%M")

                    report += (
                        f"| {item.get('industry_name')} | "
                        f"{item.get('previous_status')}→{item.get('new_status')} | "
                        f"{item.get('filename')} | "
                        f"{priority} | "
                        f"{created} |\n"
                    )

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(report)

            return True

        except Exception as e:
            print(f"Error creating approval report: {e}")
            return False
