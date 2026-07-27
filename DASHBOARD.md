# Social Media Engine - Dashboard

Professional web-based dashboard for monitoring and managing the Social Media Engine.

## Features

### 📊 Overview Tab
- **System Status** - Real-time status cards (industries tracked, status changes, pending approvals, queued posts)
- **Status Distribution** - Visual breakdown of industries by status (GREEN/YELLOW/ORANGE/RED)
- **Recent Changes** - List of industries with status changes

### 🏢 Industries Tab
- **Complete Industry Table** - All industries at a glance with:
  - Current status (color-coded)
  - Percentage change from previous quarter
  - Current revenue
  - Units sold
  - Primary product
- **Sortable and searchable** - Easy navigation

### ✅ Approvals Tab
- **Pending Approvals Queue** - Industries awaiting Tim's decision
- **Priority Indicators** - Color-coded by urgency (RED/ORANGE/YELLOW/GREEN)
- **Approval/Rejection UI** - Approve or reject from dashboard
- **Notes** - Add comments when approving/rejecting
- **Expiration Timer** - Shows when approval will auto-expire (7 days)

### 📅 Scheduling Tab
- **Queued Posts** - All approved content scheduled for posting
- **Platform Filtering** - View posts by platform (LinkedIn, Twitter, Instagram, etc.)
- **Countdown Timers** - See when each post will publish
- **Platform Groups** - Posts organized by social platform

### 📈 Performance Tab
- **Key Metrics**
  - Total posts tracked
  - Total engagement
  - Total reach
  - Average engagement rate
- **By-Platform Stats** - Performance broken down by each social platform
- **Performance Table** - Detailed metrics for each platform

---

## 🚀 Quick Start

### Option 1: Using Script (Recommended)
```bash
cd /home/user/social_media_engine
bash run_dashboard.sh
```

The script will:
- Check for Python 3 and pip3
- Install Flask dependencies
- Start the dashboard server

### Option 2: Manual Start
```bash
cd /home/user/social_media_engine
pip install flask flask-cors
python3 src/dashboard/app.py
```

### Access Dashboard
Open browser and go to:
```
http://localhost:5000
```

---

## 📱 Dashboard Layout

```
┌─────────────────────────────────────────────────┐
│  🚀 Social Media Engine                 ●--:--  │
│  Autonomous Campaign Manager                    │
├─────────────────────────────────────────────────┤
│ 📊 Overview │ 🏢 Industries │ ✅ Approvals │ ... │
├─────────────────────────────────────────────────┤
│                                                 │
│  Status Grid (4 cards)                          │
│  ┌──────────┬──────────┬──────────┬──────────┐  │
│  │Industries│  Changes │ Pending  │ Queued   │  │
│  │    8     │    3     │    2     │    15    │  │
│  └──────────┴──────────┴──────────┴──────────┘  │
│                                                 │
│  Status Distribution                            │
│  🟢 GREEN: 4  │  🟡 YELLOW: 2  │ 🟠 ORANGE: 1  │
│  🔴 RED: 1                                      │
│                                                 │
│  Recent Status Changes                          │
│  ┌─────────────────────────────────────────┐   │
│  │ ↓ Technology: GREEN → YELLOW   -5.56%  │   │
│  │ ↓ Finance: YELLOW → ORANGE   -15.00%   │   │
│  │ ↓ E-Commerce: ORANGE → RED    -26.19%  │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
├─────────────────────────────────────────────────┤
│ Social Media Engine v1.0 | Auto-refresh 30s    │
└─────────────────────────────────────────────────┘
```

---

## 🔄 Auto-Refresh

Dashboard automatically refreshes data every **30 seconds**:
- Status counts update
- New approvals appear
- Scheduled posts countdown
- Performance metrics refresh
- Live clock updates

---

## ✏️ Approval Workflow

**From Dashboard:**

1. Go to **✅ Approvals** tab
2. See pending approval card
3. Click **✅ Approve** or **❌ Reject**
4. Add optional notes
5. Confirm action
6. Card disappears from queue
7. Content scheduled or returned for revision

---

## 📊 Status Meanings

| Status | Color | Meaning | Action |
|--------|-------|---------|--------|
| **GREEN** | 🟢 | +5% or better revenue | Continue strategy |
| **YELLOW** | 🟡 | -5% to +4% revenue | Monitor, consider adjustment |
| **ORANGE** | 🟠 | -15% to -5% revenue | Prepare pivot |
| **RED** | 🔴 | -25% or worse revenue | Urgent pivot needed |

---

## 🎨 Design

- **Dark Theme** - Easy on the eyes, modern look
- **Color-Coded** - Instant visual status recognition
- **Responsive** - Works on desktop, tablet, mobile
- **Real-Time** - Live updates every 30 seconds
- **Interactive** - Approve/reject from UI

---

## 📡 API Endpoints

Dashboard uses these backend endpoints:

### Status
```
GET /api/status
Response: {
  timestamp, industries_total, status_summary,
  status_changes, workflow, scheduler
}
```

### Industries
```
GET /api/industries
Response: [ { id, name, status, percent_change, revenue_current,
              revenue_previous, units_sold, product }, ... ]
```

### Pending Approvals
```
GET /api/pending-approvals
Response: { items: [...], total: N }
```

### Scheduled Posts
```
GET /api/scheduled-posts
Response: { items: [...], by_platform: {...}, total: N }
```

### Performance
```
GET /api/performance
Response: { total_posts, total_engagement, total_reach,
            avg_engagement_rate, by_platform: {...} }
```

### Workflow Actions
```
POST /api/workflow-actions
Body: { action: "approve|reject", industry_id, notes }
Response: { success, message }
```

---

## 🔧 Configuration

Dashboard works with **sample data by default** - no configuration needed!

To use real data, configure:
- `config/settings.json` - System settings
- `data/status_report.json` - Latest status calculation
- Approval queue files in `data/approval_queue/`

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
python3 src/dashboard/app.py  # Edit app.py port=5000
```

### Module Not Found
```bash
# Install dependencies
pip install flask flask-cors
```

### Can't Connect
```bash
# Check if server is running
# Verify: http://localhost:5000
# Check console output for errors
```

### Data Not Loading
```bash
# Dashboard works with sample data by default
# If using real data, ensure files exist:
# - data/status_report.json
# - data/approval_queue/ (with .metadata/)
# - data/scheduled/
# - data/tracking/
```

---

## 📋 Sample Data

Dashboard comes with **sample data** for demo:
- 8 industries with varying statuses
- 3 status changes (Tech, Finance, E-Commerce)
- 2 pending approvals
- Various scheduled posts
- Performance metrics

**This allows you to see and test the dashboard immediately without any configuration!**

---

## 🎯 Typical Workflow

1. **View Overview** - See system status at a glance
2. **Check Industries** - View all industries and their health
3. **Review Pending** - See what needs approval
4. **Make Decisions** - Approve or reject campaigns
5. **Track Scheduling** - Monitor what's scheduled to post
6. **Analyze Performance** - Review engagement and reach

---

## 🚀 Features Roadmap

Currently Implemented:
- ✅ Real-time status overview
- ✅ Industry management table
- ✅ Approval workflow UI
- ✅ Scheduling visualization
- ✅ Performance metrics
- ✅ Auto-refresh
- ✅ Responsive design
- ✅ Sample data demo

Future Enhancements:
- 📋 Export reports to PDF
- 📊 Advanced analytics charts
- 🔔 Email notifications
- 🔐 User authentication
- 🎯 Custom dashboards
- 📱 Mobile app
- 🌐 Multi-language support

---

## 💡 Tips

**For Best Experience:**
- Use a modern browser (Chrome, Firefox, Safari, Edge)
- Keep dashboard open for real-time updates
- Use Approvals tab for quick decisions
- Check Performance tab for ROI analysis
- Review Industries table weekly

---

## 📞 Support

**Dashboard Questions?**
- See QUICK_START.md for quick reference
- See SESSION_BACKUP.md for complete documentation
- Check API endpoints above

**Ready to go live?**
1. Copy config templates
2. Add real sales data
3. Configure thresholds and cadence
4. Dashboard will load real data automatically

---

## 🎬 Getting Started

### Run Dashboard
```bash
bash run_dashboard.sh
# Open http://localhost:5000
```

### Test Approval Workflow
1. Go to **✅ Approvals** tab
2. Click **✅ Approve** on any pending item
3. Add notes (optional)
4. See approval process in action

### Explore Data
1. Check **🏢 Industries** tab
2. View **📅 Scheduling** tab
3. Review **📈 Performance** tab

---

**Dashboard Ready to Use! 🎉**

Open http://localhost:5000 and start managing your campaigns.

