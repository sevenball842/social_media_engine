// Social Media Engine - Dashboard JavaScript

class Dashboard {
    constructor() {
        this.currentModal = null;
        this.refreshInterval = 30000; // 30 seconds
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadData();
        this.updateTime();
        this.startAutoRefresh();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target));
        });

        // Modal
        const modal = document.getElementById('approval-modal');
        const closeBtn = modal.querySelector('.close');
        const cancelBtn = document.getElementById('cancel-btn');

        closeBtn.addEventListener('click', () => this.closeModal());
        cancelBtn.addEventListener('click', () => this.closeModal());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.closeModal();
        });

        // Approval buttons
        document.getElementById('approve-btn').addEventListener('click', () => this.submitApproval('approve'));
        document.getElementById('reject-btn').addEventListener('click', () => this.submitApproval('reject'));
    }

    switchTab(tab) {
        // Update nav buttons
        document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
        tab.classList.add('active');

        // Update content
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        const tabId = tab.dataset.tab + '-tab';
        document.getElementById(tabId).classList.add('active');
    }

    async loadData() {
        await Promise.all([
            this.loadStatus(),
            this.loadIndustries(),
            this.loadPendingApprovals(),
            this.loadScheduledPosts(),
            this.loadPerformance()
        ]);
    }

    async loadStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            document.getElementById('industries-total').textContent = data.industries_total;
            document.getElementById('status-changes').textContent = data.status_changes;
            document.getElementById('pending-approvals').textContent = data.workflow.pending;
            document.getElementById('queued-posts').textContent = data.scheduler.queued;

            // Status distribution
            document.getElementById('count-green').textContent = data.status_summary.GREEN || 0;
            document.getElementById('count-yellow').textContent = data.status_summary.YELLOW || 0;
            document.getElementById('count-orange').textContent = data.status_summary.ORANGE || 0;
            document.getElementById('count-red').textContent = data.status_summary.RED || 0;
        } catch (error) {
            console.error('Error loading status:', error);
        }
    }

    async loadIndustries() {
        try {
            const response = await fetch('/api/industries');
            const industries = await response.json();

            const tbody = document.getElementById('industries-tbody');
            tbody.innerHTML = '';

            // Add recent changes
            this.displayRecentChanges(industries);

            // Add to industries table
            industries.forEach(ind => {
                const row = document.createElement('tr');
                const statusClass = ind.status.toLowerCase();
                const percentClass = ind.percent_change < 0 ? 'negative' : 'positive';
                const sign = ind.percent_change < 0 ? '' : '+';

                row.innerHTML = `
                    <td>${ind.name}</td>
                    <td><span class="status-badge ${statusClass}">${ind.status}</span></td>
                    <td><span class="percent-change ${percentClass}">${sign}${ind.percent_change.toFixed(2)}%</span></td>
                    <td>$${(ind.revenue_current / 1000).toFixed(0)}k</td>
                    <td>${ind.units_sold}</td>
                    <td>${ind.product}</td>
                `;
                tbody.appendChild(row);
            });
        } catch (error) {
            console.error('Error loading industries:', error);
        }
    }

    displayRecentChanges(industries) {
        const container = document.getElementById('recent-changes');
        const changed = industries.filter(i =>
            i.status === 'RED' || i.status === 'ORANGE' || i.status === 'YELLOW'
        );

        if (changed.length === 0) {
            container.innerHTML = '<p class="loading">No significant changes</p>';
            return;
        }

        container.innerHTML = changed.map(ind => {
            const statusClass = `status-change-${ind.status.toLowerCase()}`;
            const sign = ind.percent_change < 0 ? '' : '+';
            return `
                <div class="change-item ${statusClass}">
                    <div class="change-info">
                        <div class="change-industry">${ind.name} → ${ind.status}</div>
                        <div class="change-detail">${ind.product}</div>
                    </div>
                    <div class="change-percent">${sign}${ind.percent_change.toFixed(2)}%</div>
                </div>
            `;
        }).join('');
    }

    async loadPendingApprovals() {
        try {
            const response = await fetch('/api/pending-approvals');
            const data = await response.json();
            const container = document.getElementById('approvals-list');

            if (data.total === 0) {
                container.innerHTML = '<p class="loading">No pending approvals</p>';
                return;
            }

            container.innerHTML = data.items.map(item => {
                const priorityClass = item.priority.includes('HIGH') ? 'high-priority' :
                                      item.priority.includes('MEDIUM') ? 'medium-priority' :
                                      'low-priority';
                const expiresAt = new Date(item.expires_at);
                const now = new Date();
                const hoursLeft = Math.floor((expiresAt - now) / (1000 * 60 * 60));

                return `
                    <div class="approval-card ${priorityClass}">
                        <div class="approval-info">
                            <div class="approval-industry">${item.industry_name}</div>
                            <div class="approval-details">
                                <span>${item.previous_status} → ${item.new_status}</span>
                                <span>${item.percent_change.toFixed(2)}% change</span>
                                <span>${item.priority}</span>
                                <span>Expires in ${hoursLeft}h</span>
                            </div>
                        </div>
                        <div class="approval-actions">
                            <button class="btn btn-approve" onclick="dashboard.openApprovalModal('${item.industry_id}', '${item.industry_name}', 'approve')">
                                ✅ Approve
                            </button>
                            <button class="btn btn-reject" onclick="dashboard.openApprovalModal('${item.industry_id}', '${item.industry_name}', 'reject')">
                                ❌ Reject
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        } catch (error) {
            console.error('Error loading approvals:', error);
            document.getElementById('approvals-list').innerHTML = '<p class="loading">Error loading approvals</p>';
        }
    }

    async loadScheduledPosts() {
        try {
            const response = await fetch('/api/scheduled-posts');
            const data = await response.json();
            const container = document.getElementById('scheduled-list');

            if (data.total === 0) {
                container.innerHTML = '<p class="loading">No scheduled posts yet</p>';
                return;
            }

            // Build platform tabs
            const platformTabs = document.getElementById('platform-tabs');
            platformTabs.innerHTML = Object.keys(data.by_platform).map((platform, i) => `
                <div class="platform-tab ${i === 0 ? 'active' : ''}" onclick="dashboard.filterPlatform('${platform}')">
                    ${platform.toUpperCase()} (${data.by_platform[platform].length})
                </div>
            `).join('');

            // Display posts
            const firstPlatform = Object.keys(data.by_platform)[0];
            const posts = data.by_platform[firstPlatform] || [];

            this.displayScheduledPosts(posts);
        } catch (error) {
            console.error('Error loading scheduled posts:', error);
            document.getElementById('scheduled-list').innerHTML = '<p class="loading">Error loading scheduled posts</p>';
        }
    }

    displayScheduledPosts(posts) {
        const container = document.getElementById('scheduled-list');
        container.innerHTML = posts.map(post => {
            const scheduledTime = new Date(post.scheduled_time);
            const now = new Date();
            const timeUntil = this.formatTimeUntil(scheduledTime - now);

            return `
                <div class="scheduled-item">
                    <div class="scheduled-info">
                        <div>
                            <span class="scheduled-platform">${post.platform.toUpperCase()}</span>
                            <span class="scheduled-industry">${post.industry}</span>
                        </div>
                        <div class="scheduled-time">Posting ${timeUntil}</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    filterPlatform(platform) {
        // Update tab styling
        document.querySelectorAll('.platform-tab').forEach(tab => tab.classList.remove('active'));
        event.target.classList.add('active');

        // Reload filtered posts
        fetch('/api/scheduled-posts')
            .then(r => r.json())
            .then(data => this.displayScheduledPosts(data.by_platform[platform] || []))
            .catch(e => console.error('Error filtering posts:', e));
    }

    async loadPerformance() {
        try {
            const response = await fetch('/api/performance');
            const data = await response.json();

            document.getElementById('perf-posts').textContent = data.total_posts;
            document.getElementById('perf-engagement').textContent = data.total_engagement;
            document.getElementById('perf-reach').textContent = this.formatNumber(data.total_reach);
            document.getElementById('perf-rate').textContent = data.avg_engagement_rate.toFixed(2) + '%';

            // Platform table
            const tbody = document.getElementById('platform-perf-tbody');
            tbody.innerHTML = '';

            Object.entries(data.by_platform).forEach(([platform, stats]) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${platform.toUpperCase()}</td>
                    <td>${stats.posts}</td>
                    <td>${stats.engagement}</td>
                    <td>${this.formatNumber(stats.reach)}</td>
                `;
                tbody.appendChild(row);
            });

            if (Object.keys(data.by_platform).length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="loading">No performance data yet</td></tr>';
            }
        } catch (error) {
            console.error('Error loading performance:', error);
        }
    }

    openApprovalModal(industryId, industryName, action) {
        this.currentApprovalData = { industryId, action };

        const modal = document.getElementById('approval-modal');
        document.getElementById('modal-industry').innerHTML = `
            <p><strong>${industryName}</strong></p>
            <p>Action: <em>${action.toUpperCase()}</em></p>
        `;
        document.getElementById('modal-notes').value = '';

        modal.classList.add('active');
    }

    closeModal() {
        document.getElementById('approval-modal').classList.remove('active');
        this.currentApprovalData = null;
    }

    async submitApproval(action) {
        if (!this.currentApprovalData) return;

        const notes = document.getElementById('modal-notes').value;
        const { industryId } = this.currentApprovalData;

        try {
            const response = await fetch('/api/workflow-actions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action,
                    industry_id: industryId,
                    notes
                })
            });

            const data = await response.json();
            if (data.success) {
                this.closeModal();
                this.loadPendingApprovals();
                alert(`✅ ${data.message}`);
            } else {
                alert(`❌ ${data.message}`);
            }
        } catch (error) {
            console.error('Error submitting approval:', error);
            alert('Error submitting approval');
        }
    }

    updateTime() {
        const now = new Date();
        const time = now.toLocaleTimeString();
        document.getElementById('live-time').textContent = time;
    }

    formatTimeUntil(ms) {
        if (ms < 0) return 'now';
        const hours = Math.floor(ms / (1000 * 60 * 60));
        const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));
        if (hours > 0) return `in ${hours}h ${minutes}m`;
        return `in ${minutes}m`;
    }

    formatNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }

    startAutoRefresh() {
        setInterval(() => {
            this.loadData();
            this.updateTime();
        }, this.refreshInterval);

        // Update time every second
        setInterval(() => this.updateTime(), 1000);
    }
}

// Initialize dashboard on page load
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new Dashboard();
});
