"""Social Media Engine - Web Dashboard"""

import json
import os
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from status_calculator import StatusCalculator
from approval_workflow import ApprovalWorkflow
from scheduler import Scheduler
from performance_tracker import PerformanceTracker

app = Flask(__name__, template_folder="templates", static_folder="static")

# Configuration
app.config["JSON_SORT_KEYS"] = False
QUEUE_DIR = "data/approval_queue/"


# ============================================================================
# ROUTES
# ============================================================================


@app.route("/")
def dashboard():
    """Main dashboard page"""
    return render_template("dashboard.html")


@app.route("/api/status")
def api_status():
    """Get overall system status"""
    try:
        # Load sample status report
        status_report_path = "data/status_report.json"
        if os.path.exists(status_report_path):
            with open(status_report_path, "r") as f:
                report = json.load(f)
        else:
            report = _generate_sample_status()

        # Get workflow status
        workflow = ApprovalWorkflow(QUEUE_DIR)
        w_status = workflow.get_workflow_status()

        # Get scheduler status
        scheduler = Scheduler()
        s_status = scheduler.get_posting_status()

        # Combine
        status = {
            "timestamp": datetime.now().isoformat(),
            "industries_total": report.get("total_industries", 0),
            "status_summary": report.get("status_summary", {}),
            "status_changes": len(report.get("status_changes", [])),
            "workflow": {
                "pending": w_status["status_summary"].get("pending", 0),
                "approved": w_status["status_summary"].get("approved", 0),
                "rejected": w_status["status_summary"].get("rejected", 0),
            },
            "scheduler": {
                "queued": s_status["scheduled_count"],
                "posted": s_status["posted_count"],
            },
        }

        return jsonify(status)
    except Exception as e:
        print(f"Error in api_status: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/industries")
def api_industries():
    """Get all industries and their status"""
    try:
        status_report_path = "data/status_report.json"
        if os.path.exists(status_report_path):
            with open(status_report_path, "r") as f:
                report = json.load(f)
        else:
            report = _generate_sample_status()

        industries = []
        for industry_id, data in report.get("industries", {}).items():
            industries.append(
                {
                    "id": industry_id,
                    "name": data.get("name", industry_id),
                    "status": data.get("status", "UNKNOWN"),
                    "percent_change": data.get("percent_change", 0),
                    "revenue_current": data.get("current_quarter_revenue", 0),
                    "revenue_previous": data.get("previous_quarter_revenue", 0),
                    "units_sold": data.get("units_sold", 0),
                    "product": data.get("primary_product", "Web Scanning Tool"),
                }
            )

        # Sort by status (RED first)
        status_order = {"RED": 0, "ORANGE": 1, "YELLOW": 2, "GREEN": 3}
        industries.sort(key=lambda x: status_order.get(x["status"], 4))

        return jsonify(industries)
    except Exception as e:
        print(f"Error in api_industries: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/pending-approvals")
def api_pending_approvals():
    """Get pending approval items"""
    try:
        workflow = ApprovalWorkflow(QUEUE_DIR)
        pending = workflow.get_pending_items()

        items = []
        for item in pending:
            items.append(
                {
                    "industry_id": item.get("industry_id"),
                    "industry_name": item.get("industry_name"),
                    "previous_status": item.get("previous_status"),
                    "new_status": item.get("new_status"),
                    "percent_change": item.get("percent_change"),
                    "created_at": item.get("created_at"),
                    "expires_at": item.get("expires_at"),
                    "filename": item.get("filename"),
                    "priority": _get_priority(item.get("new_status", "GREEN")),
                }
            )

        return jsonify({"items": items, "total": len(items)})
    except Exception as e:
        print(f"Error in api_pending_approvals: {e}")
        return jsonify({"error": str(e), "items": [], "total": 0}), 500


@app.route("/api/scheduled-posts")
def api_scheduled_posts():
    """Get currently scheduled posts"""
    try:
        scheduler = Scheduler()
        posts = scheduler.get_scheduled_posts()

        items = []
        for post in posts:
            items.append(
                {
                    "id": post.get("id"),
                    "platform": post.get("platform"),
                    "industry": post.get("industry"),
                    "scheduled_time": post.get("scheduled_time"),
                    "status": post.get("status"),
                }
            )

        # Group by platform
        by_platform = {}
        for post in items:
            platform = post["platform"]
            if platform not in by_platform:
                by_platform[platform] = []
            by_platform[platform].append(post)

        return jsonify({"items": items, "by_platform": by_platform, "total": len(items)})
    except Exception as e:
        print(f"Error in api_scheduled_posts: {e}")
        return jsonify({"error": str(e), "items": [], "by_platform": {}, "total": 0}), 500


@app.route("/api/performance")
def api_performance():
    """Get performance summary"""
    try:
        tracker = PerformanceTracker()
        stats = tracker.get_summary_stats()

        return jsonify(
            {
                "total_posts": stats.get("total_posts", 0),
                "total_engagement": stats.get("total_engagement", 0),
                "total_reach": stats.get("total_reach", 0),
                "avg_engagement_rate": stats.get("avg_engagement_rate", 0),
                "by_platform": stats.get("by_platform", {}),
            }
        )
    except Exception as e:
        print(f"Error in api_performance: {e}")
        return jsonify(
            {
                "total_posts": 0,
                "total_engagement": 0,
                "total_reach": 0,
                "avg_engagement_rate": 0,
                "by_platform": {},
                "error": str(e),
            }
        ), 500


@app.route("/api/workflow-actions", methods=["POST"])
def api_workflow_actions():
    """Handle workflow actions (approve/reject)"""
    try:
        data = request.json
        action = data.get("action")
        industry_id = data.get("industry_id")
        notes = data.get("notes", "")

        workflow = ApprovalWorkflow(QUEUE_DIR)

        if action == "approve":
            success = workflow.approve_pivot(industry_id, notes)
            message = f"Approved: {industry_id}" if success else "Failed to approve"
        elif action == "reject":
            success = workflow.reject_pivot(industry_id, notes)
            message = f"Rejected: {industry_id}" if success else "Failed to reject"
        else:
            return jsonify({"success": False, "message": "Unknown action"}), 400

        return jsonify({"success": success, "message": message})
    except Exception as e:
        print(f"Error in api_workflow_actions: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _get_priority(status):
    """Get priority level based on status"""
    return {
        "RED": "🔴 HIGH",
        "ORANGE": "🟠 HIGH",
        "YELLOW": "🟡 MEDIUM",
        "GREEN": "🟢 LOW",
    }.get(status, "❓ UNKNOWN")


def _generate_sample_status():
    """Generate sample status report for demo purposes"""
    return {
        "timestamp": datetime.now().isoformat(),
        "total_industries": 8,
        "status_summary": {"GREEN": 4, "YELLOW": 2, "ORANGE": 1, "RED": 1},
        "status_changes_count": 3,
        "status_changes": [
            {
                "industry_id": "tech",
                "industry_name": "Technology",
                "previous_status": "GREEN",
                "new_status": "YELLOW",
                "percent_change": -5.56,
            },
            {
                "industry_id": "finance",
                "industry_name": "Finance",
                "previous_status": "YELLOW",
                "new_status": "ORANGE",
                "percent_change": -15.0,
            },
            {
                "industry_id": "ecommerce",
                "industry_name": "E-Commerce",
                "previous_status": "ORANGE",
                "new_status": "RED",
                "percent_change": -26.19,
            },
        ],
        "industries": {
            "tech": {
                "name": "Technology",
                "status": "YELLOW",
                "percent_change": -5.56,
                "current_quarter_revenue": 425000,
                "previous_quarter_revenue": 450000,
                "units_sold": 1200,
                "primary_product": "Web Scanning Tool",
            },
            "healthcare": {
                "name": "Healthcare",
                "status": "GREEN",
                "percent_change": 7.81,
                "current_quarter_revenue": 345000,
                "previous_quarter_revenue": 320000,
                "units_sold": 890,
                "primary_product": "Compliance Scanner",
            },
            "finance": {
                "name": "Finance",
                "status": "ORANGE",
                "percent_change": -15.0,
                "current_quarter_revenue": 238000,
                "previous_quarter_revenue": 280000,
                "units_sold": 650,
                "primary_product": "Regulatory Compliance Tool",
            },
            "ecommerce": {
                "name": "E-Commerce",
                "status": "RED",
                "percent_change": -26.19,
                "current_quarter_revenue": 155000,
                "previous_quarter_revenue": 210000,
                "units_sold": 380,
                "primary_product": "E-Commerce Compliance Scanner",
            },
            "education": {
                "name": "Education",
                "status": "GREEN",
                "percent_change": 5.71,
                "current_quarter_revenue": 185000,
                "previous_quarter_revenue": 175000,
                "units_sold": 520,
                "primary_product": "Educational Compliance Tool",
            },
            "enterprise": {
                "name": "Enterprise",
                "status": "GREEN",
                "percent_change": 6.79,
                "current_quarter_revenue": 598000,
                "previous_quarter_revenue": 560000,
                "units_sold": 1450,
                "primary_product": "Enterprise Web Scanner",
            },
            "startup": {
                "name": "Startup",
                "status": "YELLOW",
                "percent_change": -10.53,
                "current_quarter_revenue": 85000,
                "previous_quarter_revenue": 95000,
                "units_sold": 210,
                "primary_product": "Startup Compliance Package",
            },
            "nonprofit": {
                "name": "Nonprofit",
                "status": "GREEN",
                "percent_change": 10.77,
                "current_quarter_revenue": 72000,
                "previous_quarter_revenue": 65000,
                "units_sold": 140,
                "primary_product": "Nonprofit Compliance Scanner",
            },
        },
    }


if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    os.makedirs("src/dashboard/templates", exist_ok=True)
    os.makedirs("src/dashboard/static", exist_ok=True)

    print("🚀 Starting Social Media Engine Dashboard...")
    print("📊 Open browser: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
