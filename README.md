# Social Media Engine

Autonomous social media campaign system that pivots content strategy based on quarterly sales performance.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Sales Data Input (Quarterly)                 │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│              Status Calculator (% Change Logic)                  │
│    GREEN → YELLOW → ORANGE → RED (by industry)                  │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│            Scan External Repos & Import Schedules               │
│       (existing materials, pre-built content, cadence)          │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│           Merge Existing Schedule + New Pivots                  │
│        (identify changed industries, prep alternatives)         │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│        Generate Campaign Pivot MD Files for Tim Review          │
│          (options, messaging, timing, performance est.)         │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│              Tim Approves/Edits Pivots (Workflow)               │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│           Post Approved Content Per Cadence                     │
│        (multi-platform: LinkedIn, Twitter, Instagram, etc.)     │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│          Track Performance & Historical Data                    │
│    (engagement, reach, effectiveness per industry/campaign)     │
└─────────────────────────────────────────────────────────────────┘
```

## Key Features

- **Data-Driven Pivots**: Quarterly sales performance drives campaign strategy
- **External Repo Integration**: Scans and imports existing schedules and materials
- **Approval Workflow**: All content reviewed by Tim before posting (100% approval authority)
- **Multi-Platform**: LinkedIn, Twitter, Instagram, Facebook, TikTok
- **Performance Tracking**: Historical data, engagement metrics, ROI analysis
- **Dashboard**: Real-time status by industry, change alerts, content queue

## Quick Start

```bash
# 1. Configure system
cp config/settings.template.json config/settings.json
# Edit settings.json with your values

# 2. Add quarterly sales data
cp data/sales_data/Q1_2026.template.json data/sales_data/Q1_2026.json

# 3. Run status calculation
python src/status_calculator/run.py

# 4. Import existing schedule from external repo
python src/data_importer/scan_repo.py --repo https://github.com/you/existing-schedule

# 5. Generate campaign pivots
python src/content_generator/generate_pivots.py

# 6. Review MD files in approval_queue/
# 7. Approve in workflow dashboard
# 8. Post on schedule
```

## Project Structure

```
social_media_engine/
├── README.md (this file)
├── config/                    # Configuration files
│   ├── settings.template.json
│   ├── settings.json
│   └── industries.json
├── src/                       # Core Python modules
│   ├── __init__.py
│   ├── dashboard/             # Dashboard & visualizations
│   ├── status_calculator/     # % change logic, thresholds
│   ├── data_importer/         # Scan & import external repos
│   ├── content_generator/     # Generate pivot MD files
│   ├── approval_workflow/     # Tim's review/approval system
│   ├── scheduler/             # Post on cadence
│   └── performance_tracker/   # Analytics & historical data
├── data/
│   ├── sales_data/            # Quarterly reports
│   ├── schedules/             # Imported content schedules
│   ├── tracking/              # Historical performance
│   └── approval_queue/        # MD files awaiting Tim review
├── templates/
│   ├── campaign_pivot.md      # Template for pivot MD files
│   └── sales_report.json      # Template for sales data
├── tests/                     # Unit & integration tests
└── docs/                      # Documentation
```

## Configuration

Edit `config/settings.json` to customize:
- API keys (GitHub, social platforms, etc.)
- Status thresholds (GREEN/YELLOW/ORANGE/RED % changes)
- Posting cadence (frequency per platform)
- Industries to track
- Approval email/notifications
- Performance tracking preferences

## Usage

### 1. Ingest Quarterly Sales Data
```bash
python src/status_calculator/run.py --data data/sales_data/Q2_2026.json
```

### 2. Scan External Repository for Existing Schedule
```bash
python src/data_importer/scan_repo.py \
  --repo https://github.com/owner/existing-schedule-repo \
  --token YOUR_GITHUB_TOKEN
```

### 3. Calculate Status Changes & Generate Pivots
```bash
python src/content_generator/generate_pivots.py
```

### 4. Review Dashboard
```bash
python src/dashboard/app.py  # Opens dashboard at http://localhost:5000
```

### 5. Check Approval Queue
```bash
ls -la data/approval_queue/
```

### 6. Approve & Schedule (via workflow)
```bash
python src/approval_workflow/submit_approval.py --file data/approval_queue/industry_pivot_Q2.md
```

### 7. Post Content
```bash
python src/scheduler/run_schedule.py --dry-run  # Preview
python src/scheduler/run_schedule.py             # Actually post
```

### 8. Track Performance
```bash
python src/performance_tracker/report.py  # Generate performance report
```

## Workflow

1. **Tim uploads quarterly sales data** → Engine ingests and calculates status changes
2. **Engine scans external repo** → Imports existing content schedule and materials
3. **Engine identifies changed industries** → Merges with existing schedule, flags pivots needed
4. **Pivot MD files generated** → Stored in `data/approval_queue/`
5. **Tim reviews MD files** → Approves, edits, or requests regeneration
6. **Approved content queued** → Scheduled per cadence settings
7. **Content auto-posts** → Per approved schedule across platforms
8. **Performance tracked** → Engagement, reach, effectiveness recorded

## Approval Authority

✅ **100% Tim Approval Required** - No autonomous posting  
✅ **Tim maintains full control** - Can edit, reject, or request regeneration  
✅ **Engine autonomous in prep** - Not in execution  

## Platforms Supported

- LinkedIn
- Twitter/X
- Instagram
- Facebook
- TikTok
- YouTube (video content)

## Data Flow

```
Sales Data (Quarterly)
    ↓
Status Calculation (% changes by industry)
    ↓
External Repo Scan (existing schedule + materials)
    ↓
Merge & Identify Pivots
    ↓
Generate Pivot Options (MD files)
    ↓
Tim's Approval Workflow
    ↓
Scheduling System (posts per cadence)
    ↓
Performance Tracking (analytics & historical)
    ↓
Dashboard (real-time status & alerts)
```

## Next Steps

1. Configure `config/settings.json` with thresholds and API keys
2. Add sample quarterly sales data to `data/sales_data/`
3. Provide external repo URL for existing schedule
4. Define industries to track in `config/industries.json`
5. Run initial status calculation
6. Test approval workflow with sample data

## Questions?

See `/docs` for detailed documentation on each module.

---

**Status**: Ready to build  
**Owner**: Tim (Director of Operations)  
**Marketing Lead**: Allie Rae  
**Tech Lead**: Claude Code
