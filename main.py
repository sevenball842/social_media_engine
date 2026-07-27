#!/usr/bin/env python3
"""
Social Media Engine - Main entry point

Coordinates the entire workflow:
1. Ingest quarterly sales data
2. Calculate status changes
3. Scan external repo for existing schedule
4. Merge with new pivots
5. Generate approval documents
6. Manage approval workflow
7. Schedule approved content
8. Track performance
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from status_calculator import StatusCalculator
from data_importer import DataImporter
from content_generator import ContentGenerator
from approval_workflow import ApprovalWorkflow
from scheduler import Scheduler
from performance_tracker import PerformanceTracker
from utils import load_config


def main():
    parser = argparse.ArgumentParser(
        description="Social Media Engine - Automated campaign management"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Calculate status command
    calc_parser = subparsers.add_parser("calculate", help="Calculate status from sales data")
    calc_parser.add_argument("--data", required=True, help="Path to sales data JSON")
    calc_parser.add_argument("--config", default="config/settings.json", help="Config file")

    # Import schedule command
    import_parser = subparsers.add_parser(
        "import", help="Import schedule from external repo"
    )
    import_parser.add_argument("--repo", required=True, help="External repo URL")
    import_parser.add_argument("--branch", default="main", help="Git branch")
    import_parser.add_argument("--token", help="GitHub token (for private repos)")
    import_parser.add_argument("--output", default="data/imported_schedule.json", help="Output file")

    # Generate pivots command
    gen_parser = subparsers.add_parser("generate", help="Generate campaign pivot files")
    gen_parser.add_argument("--status-report", required=True, help="Status report JSON")
    gen_parser.add_argument("--output-dir", default="data/approval_queue/", help="Output directory")
    gen_parser.add_argument("--template", default="templates/campaign_pivot.md", help="Template file")

    # Approval workflow command
    approve_parser = subparsers.add_parser("workflow", help="Manage approval workflow")
    approve_parser.add_argument(
        "--action",
        choices=["status", "pending", "approve", "reject"],
        required=True,
        help="Workflow action",
    )
    approve_parser.add_argument("--industry", help="Industry ID (for approve/reject)")
    approve_parser.add_argument("--notes", default="", help="Notes for approval/rejection")
    approve_parser.add_argument("--queue-dir", default="data/approval_queue/", help="Queue directory")

    # Schedule command
    schedule_parser = subparsers.add_parser("schedule", help="Queue approved content for posting")
    schedule_parser.add_argument("--config", default="config/settings.json", help="Config file")
    schedule_parser.add_argument("--workflow-dir", default="data/approval_queue/", help="Workflow directory")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show system status")
    status_parser.add_argument("--all", action="store_true", help="Show all details")

    # Full pipeline command
    pipeline_parser = subparsers.add_parser("run", help="Run complete pipeline")
    pipeline_parser.add_argument("--data", required=True, help="Path to sales data JSON")
    pipeline_parser.add_argument("--repo", help="External repo URL for schedule import")
    pipeline_parser.add_argument("--config", default="config/settings.json", help="Config file")
    pipeline_parser.add_argument("--token", help="GitHub token")
    pipeline_parser.add_argument("--dry-run", action="store_true", help="Preview only")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "calculate":
            handle_calculate(args)
        elif args.command == "import":
            handle_import(args)
        elif args.command == "generate":
            handle_generate(args)
        elif args.command == "workflow":
            handle_workflow(args)
        elif args.command == "schedule":
            handle_schedule(args)
        elif args.command == "status":
            handle_status(args)
        elif args.command == "run":
            handle_pipeline(args)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def handle_calculate(args):
    """Handle status calculation."""
    print("📊 Calculating status from sales data...")

    config = load_config(args.config)
    thresholds = config.get("status_thresholds", {})

    calculator = StatusCalculator(thresholds)
    report = calculator.run_calculation(args.data, thresholds)

    print(f"✅ Status calculated for {report['total_industries']} industries")
    print(f"   - Status changes: {report['status_changes_count']}")
    print(f"   - GREEN: {report['status_summary']['GREEN']}")
    print(f"   - YELLOW: {report['status_summary']['YELLOW']}")
    print(f"   - ORANGE: {report['status_summary']['ORANGE']}")
    print(f"   - RED: {report['status_summary']['RED']}")

    # Save report
    report_path = "data/status_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"📁 Report saved to {report_path}")

    if report["status_changes"]:
        print("\n🚨 Industries with status changes:")
        for change in report["status_changes"]:
            print(
                f"   {change['industry_name']}: "
                f"{change['previous_status']} → {change['new_status']} "
                f"({change['percent_change']:+.1f}%)"
            )


def handle_import(args):
    """Handle external schedule import."""
    print(f"📥 Importing schedule from {args.repo}...")

    importer = DataImporter(args.repo, args.branch, args.token)
    schedule, materials, posts = importer.import_full_schedule()

    print(f"✅ Import successful")
    print(f"   - Posts in schedule: {len(posts)}")
    print(f"   - Materials found: {len(materials.get('files', []))}")

    # Save imported data
    output = {
        "timestamp": datetime.now().isoformat(),
        "source": args.repo,
        "schedule": schedule,
        "materials": materials,
        "posts": posts,
    }

    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"📁 Data saved to {args.output}")


def handle_generate(args):
    """Handle pivot generation."""
    print("📝 Generating campaign pivots...")

    with open(args.status_report, "r") as f:
        report = json.load(f)

    generator = ContentGenerator(args.template)
    results = generator.generate_batch_pivots(report["status_changes"], args.output_dir)

    print(f"✅ Generated {results['successful']} pivot files")
    if results["failed"]:
        print(f"⚠️  Failed to generate {results['failed']} files")

    # Create index
    generator.create_summary_index(report["status_changes"])
    print(f"📁 Index created at {args.output_dir}/INDEX.md")


def handle_workflow(args):
    """Handle approval workflow."""
    workflow = ApprovalWorkflow(args.queue_dir)

    if args.action == "status":
        status = workflow.get_workflow_status()
        print("\n📋 Workflow Status:")
        print(f"   - Pending: {status['status_summary']['pending']}")
        print(f"   - Approved: {status['status_summary']['approved']}")
        print(f"   - Rejected: {status['status_summary']['rejected']}")

    elif args.action == "pending":
        pending = workflow.get_pending_items()
        print(f"\n⏳ {len(pending)} items pending approval:")
        for item in pending:
            print(
                f"   - {item['industry_name']}: "
                f"{item['previous_status']} → {item['new_status']}"
            )

    elif args.action == "approve":
        if workflow.approve_pivot(args.industry, args.notes):
            print(f"✅ Approved: {args.industry}")
        else:
            print(f"❌ Failed to approve: {args.industry}")

    elif args.action == "reject":
        if workflow.reject_pivot(args.industry, args.notes):
            print(f"❌ Rejected: {args.industry}")
        else:
            print(f"❌ Failed to reject: {args.industry}")

    # Show updated status
    workflow.create_approval_report()
    print("📁 Approval report saved to data/approval_status.md")


def handle_schedule(args):
    """Handle content scheduling."""
    print("📅 Scheduling approved content...")

    config = load_config(args.config)
    workflow = ApprovalWorkflow(args.workflow_dir)
    scheduler = Scheduler(config)

    approved = workflow.get_approved_pivots()
    results = scheduler.queue_posts(approved)

    print(f"✅ Queued {results['posts_queued']} posts")
    for platform, count in results["by_platform"].items():
        print(f"   - {platform}: {count}")

    if results["next_post_window"]:
        print(f"📤 Next post: {results['next_post_window']}")


def handle_status(args):
    """Show system status."""
    print("\n📊 Social Media Engine Status\n")

    # Workflow status
    workflow = ApprovalWorkflow()
    w_status = workflow.get_workflow_status()
    print("Approval Workflow:")
    print(f"  - Pending: {w_status['status_summary']['pending']}")
    print(f"  - Approved: {w_status['status_summary']['approved']}")

    # Scheduler status
    scheduler = Scheduler()
    s_status = scheduler.get_posting_status()
    print("\nScheduling:")
    print(f"  - Queued: {s_status['scheduled_count']}")
    print(f"  - Posted: {s_status['posted_count']}")

    # Performance
    tracker = PerformanceTracker()
    p_stats = tracker.get_summary_stats()
    print("\nPerformance:")
    print(f"  - Posts tracked: {p_stats.get('total_posts', 0)}")
    print(f"  - Avg engagement: {p_stats.get('avg_engagement_rate', 0):.1f}%")


def handle_pipeline(args):
    """Run complete pipeline."""
    print("🚀 Running complete pipeline...\n")

    # 1. Calculate status
    print("1️⃣  Calculating status...")
    config = load_config(args.config)
    thresholds = config.get("status_thresholds", {})
    calculator = StatusCalculator(thresholds)
    report = calculator.run_calculation(args.data, thresholds)

    with open("data/status_report.json", "w") as f:
        json.dump(report, f, indent=2)

    if not report["status_changes"]:
        print("   ℹ️  No status changes detected")
        return

    # 2. Import external schedule (if provided)
    if args.repo:
        print("2️⃣  Importing external schedule...")
        importer = DataImporter(args.repo, token=args.token)
        schedule, materials, posts = importer.import_full_schedule()
        print(f"   ✅ Imported {len(posts)} existing posts")

    # 3. Generate pivots
    print("3️⃣  Generating campaign pivots...")
    generator = ContentGenerator()
    results = generator.generate_batch_pivots(report["status_changes"])
    generator.create_summary_index(report["status_changes"])
    print(f"   ✅ Created {results['successful']} pivot files")

    # 4. Setup approval workflow
    print("4️⃣  Setting up approval workflow...")
    workflow = ApprovalWorkflow()
    for change in report["status_changes"]:
        workflow.create_pending_item(
            f"{change['industry_id']}_pivot.md",
            change["industry_id"],
            change,
        )
    print(f"   ✅ Created {len(report['status_changes'])} approval items")

    # 5. Show approval queue
    print("\n5️⃣  Approval Queue Ready:")
    pending = workflow.get_pending_items()
    for item in pending:
        print(f"   ⏳ {item['industry_name']}: {item['previous_status']} → {item['new_status']}")

    if not args.dry_run:
        print("\n✅ Pipeline complete. Awaiting Tim's approval.")
        print("   Next: python main.py workflow --action pending")
    else:
        print("\n✅ Pipeline dry-run complete (no changes committed)")


if __name__ == "__main__":
    main()
