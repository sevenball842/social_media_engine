"""Core status calculation logic."""

import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class StatusCalculator:
    """
    Calculates industry status (GREEN/YELLOW/ORANGE/RED) based on sales data.

    Status transitions:
    - GREEN: +5% or better
    - YELLOW: -5% to +4%
    - ORANGE: -15% to -5%
    - RED: -25% or worse
    """

    def __init__(self, thresholds: Optional[Dict] = None):
        """
        Initialize calculator with threshold values.

        Args:
            thresholds: Dict with keys:
                - green_to_yellow: % change threshold (default: -5)
                - yellow_to_orange: % change threshold (default: -15)
                - orange_to_red: % change threshold (default: -25)
        """
        if thresholds is None:
            thresholds = {
                "green_to_yellow": -5,
                "yellow_to_orange": -15,
                "orange_to_red": -25,
            }
        self.thresholds = thresholds

    def calculate_percent_change(
        self, previous: float, current: float
    ) -> float:
        """Calculate percentage change between two values."""
        if previous == 0:
            return 0.0
        return ((current - previous) / previous) * 100

    def get_status(self, percent_change: float) -> str:
        """
        Determine status based on percent change.

        Args:
            percent_change: Percentage change value

        Returns:
            Status string: GREEN, YELLOW, ORANGE, or RED
        """
        if percent_change >= self.thresholds["green_to_yellow"]:
            return "GREEN"
        elif percent_change >= self.thresholds["yellow_to_orange"]:
            return "YELLOW"
        elif percent_change >= self.thresholds["orange_to_red"]:
            return "ORANGE"
        else:
            return "RED"

    def process_sales_data(
        self, sales_data: Dict
    ) -> Tuple[Dict, List[Dict]]:
        """
        Process quarterly sales data and calculate status changes.

        Args:
            sales_data: Sales report dict with structure from template

        Returns:
            Tuple of (updated_industries, status_changes)
            - updated_industries: Dict of industries with new status
            - status_changes: List of industries with status changes
        """
        updated_industries = {}
        status_changes = []

        industries = sales_data.get("industries", {})

        for industry_id, data in industries.items():
            prev_revenue = data.get("previous_quarter_revenue", 0)
            curr_revenue = data.get("current_quarter_revenue", 0)

            # Calculate percent change
            pct_change = self.calculate_percent_change(prev_revenue, curr_revenue)

            # Determine new status
            new_status = self.get_status(pct_change)

            # Track old status for comparison
            old_status = data.get("status", "UNKNOWN")

            # Update data
            updated_industries[industry_id] = {
                **data,
                "percent_change": round(pct_change, 2),
                "status": new_status,
                "last_calculation": datetime.now().isoformat(),
            }

            # Record if status changed
            if old_status != new_status and old_status != "UNKNOWN":
                status_changes.append(
                    {
                        "industry_id": industry_id,
                        "industry_name": data.get("name", industry_id),
                        "previous_status": old_status,
                        "new_status": new_status,
                        "percent_change": round(pct_change, 2),
                        "previous_revenue": prev_revenue,
                        "current_revenue": curr_revenue,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        return updated_industries, status_changes

    def generate_status_report(
        self, updated_industries: Dict, status_changes: List[Dict]
    ) -> Dict:
        """
        Generate a comprehensive status report.

        Args:
            updated_industries: Output from process_sales_data
            status_changes: Output from process_sales_data

        Returns:
            Status report dict
        """
        status_counts = {
            "GREEN": 0,
            "YELLOW": 0,
            "ORANGE": 0,
            "RED": 0,
        }

        for industry_data in updated_industries.values():
            status = industry_data.get("status", "UNKNOWN")
            if status in status_counts:
                status_counts[status] += 1

        return {
            "timestamp": datetime.now().isoformat(),
            "total_industries": len(updated_industries),
            "status_summary": status_counts,
            "status_changes_count": len(status_changes),
            "status_changes": status_changes,
            "industries": updated_industries,
        }


def run_calculation(sales_data_path: str, thresholds: Optional[Dict] = None) -> Dict:
    """
    Convenience function to run status calculation from sales data file.

    Args:
        sales_data_path: Path to quarterly sales data JSON file
        thresholds: Optional threshold overrides

    Returns:
        Status report
    """
    with open(sales_data_path, "r") as f:
        sales_data = json.load(f)

    calculator = StatusCalculator(thresholds)
    updated_industries, status_changes = calculator.process_sales_data(sales_data)
    report = calculator.generate_status_report(updated_industries, status_changes)

    return report
