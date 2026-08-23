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

        // Content library events
        const uploadBtn = document.getElementById('upload-btn');
        if (uploadBtn) uploadBtn.addEventListener('click', () => this.uploadContent());

        const libSearch = document.getElementById('library-search');
        if (libSearch) libSearch.addEventListener('keyup', (e) => this.searchContent(e.target.value));

        const libFilter = document.getElementById('library-filter-category');
        if (libFilter) libFilter.addEventListener('change', (e) => this.filterContentByCategory(e.target.value));

        // Content creator events
        const creatorSaveBtn = document.getElementById('creator-save-btn');
        if (creatorSaveBtn) creatorSaveBtn.addEventListener('click', () => this.saveDraft());

        const creatorSubmitBtn = document.getElementById('creator-submit-btn');
        if (creatorSubmitBtn) creatorSubmitBtn.addEventListener('click', () => this.submitContent());
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
            this.loadPerformance(),
            this.loadContentLibrary()
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

    // Content Library Methods
    async loadContentLibrary() {
        try {
            const response = await fetch('/api/content-library');
            const data = await response.json();

            // Update stats
            document.getElementById('lib-total-items').textContent = data.stats.total_items;
            document.getElementById('lib-total-size').textContent = data.stats.total_size_mb + ' MB';
            document.getElementById('lib-industries').textContent = data.stats.industries.length;

            // Display materials grid
            this.displayContentGrid(data.items);
        } catch (error) {
            console.error('Error loading content library:', error);
        }
    }

    displayContentGrid(items) {
        const grid = document.getElementById('content-grid');
        if (!items || items.length === 0) {
            grid.innerHTML = '<p class="loading">No materials uploaded yet</p>';
            return;
        }

        grid.innerHTML = '';
        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'content-card';
            const tags = item.tags && item.tags.length > 0
                ? item.tags.map(t => `<span class="content-tag">${t}</span>`).join('')
                : '';

            card.innerHTML = `
                <div class="content-card-header">
                    <h3 class="content-card-title">${this.escapeHtml(item.title)}</h3>
                    <span class="content-card-category">${item.category.toUpperCase()}</span>
                </div>
                <div class="content-card-info">
                    <p>📅 ${new Date(item.uploaded_at).toLocaleDateString()}</p>
                    <p>💾 ${(item.file_size / 1024).toFixed(1)} KB</p>
                </div>
                ${item.description ? `<p class="content-card-description">${this.escapeHtml(item.description)}</p>` : ''}
                ${tags ? `<div class="content-card-tags">${tags}</div>` : ''}
                <div class="content-card-actions">
                    <button class="btn btn-small" onclick="dashboard.useContent('${item.id}')">📌 Use</button>
                    <button class="btn btn-small btn-danger" onclick="dashboard.deleteContent('${item.id}')">🗑️ Delete</button>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    async uploadContent() {
        const fileInput = document.getElementById('content-file');
        const title = document.getElementById('content-title').value;
        const category = document.getElementById('content-category').value;
        const industry = document.getElementById('content-industry').value;
        const description = document.getElementById('content-description').value;
        const tags = document.getElementById('content-tags').value;

        if (!fileInput.files.length) {
            alert('Please select a file');
            return;
        }

        if (!title) {
            alert('Please enter a title');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('title', title);
        formData.append('category', category);
        formData.append('industry', industry);
        formData.append('description', description);
        formData.append('tags', tags);

        try {
            const response = await fetch('/api/content-library/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.success) {
                alert('✅ Material uploaded successfully!');
                // Clear form
                document.getElementById('content-file').value = '';
                document.getElementById('content-title').value = '';
                document.getElementById('content-description').value = '';
                document.getElementById('content-tags').value = '';
                // Reload library
                this.loadContentLibrary();
            } else {
                alert(`❌ Upload failed: ${data.error}`);
            }
        } catch (error) {
            console.error('Error uploading content:', error);
            alert('Error uploading content');
        }
    }

    async searchContent(query) {
        if (!query) {
            this.loadContentLibrary();
            return;
        }

        try {
            const response = await fetch(`/api/content-library/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.displayContentGrid(data.items);
        } catch (error) {
            console.error('Error searching content:', error);
        }
    }

    async filterContentByCategory(category) {
        try {
            const url = category
                ? `/api/content-library?category=${encodeURIComponent(category)}`
                : '/api/content-library';
            const response = await fetch(url);
            const data = await response.json();
            this.displayContentGrid(data.items);
        } catch (error) {
            console.error('Error filtering content:', error);
        }
    }

    async deleteContent(itemId) {
        if (!confirm('Are you sure you want to delete this material?')) return;

        try {
            const response = await fetch(`/api/content-library/${itemId}`, {
                method: 'DELETE'
            });

            const data = await response.json();
            if (data.success) {
                alert('✅ Material deleted');
                this.loadContentLibrary();
            } else {
                alert(`❌ ${data.error}`);
            }
        } catch (error) {
            console.error('Error deleting content:', error);
        }
    }

    useContent(itemId) {
        alert(`📌 Material ${itemId} ready to use!\n\nThis would be used when scheduling posts to select pre-created materials.`);
    }

    // Content Creator Methods
    async saveDraft() {
        const campaign = document.getElementById('creator-campaign-name').value;
        const content = document.getElementById('creator-content').value;

        if (!campaign || !content) {
            alert('Please fill in campaign name and content');
            return;
        }

        // Save to localStorage for demo
        const drafts = JSON.parse(localStorage.getItem('content-drafts') || '[]');
        drafts.unshift({
            id: Date.now(),
            campaign,
            content,
            created: new Date().toLocaleString(),
            status: 'draft'
        });
        localStorage.setItem('content-drafts', JSON.stringify(drafts.slice(0, 10)));

        alert('✅ Draft saved successfully!');
        this.loadDrafts();
        document.getElementById('creator-campaign-name').value = '';
        document.getElementById('creator-content').value = '';
    }

    async submitContent() {
        const campaign = document.getElementById('creator-campaign-name').value;
        const content = document.getElementById('creator-content').value;
        const platforms = Array.from(document.querySelectorAll('.platform-checkboxes input:checked'))
            .map(cb => cb.value);

        if (!campaign || !content || platforms.length === 0) {
            alert('Please fill in all required fields and select at least one platform');
            return;
        }

        alert(`✅ Content submitted for approval!\n\nCampaign: ${campaign}\nPlatforms: ${platforms.join(', ')}\n\nThis will appear in the Approvals tab for your review.`);
        document.getElementById('creator-campaign-name').value = '';
        document.getElementById('creator-content').value = '';
        document.querySelectorAll('.platform-checkboxes input').forEach(cb => cb.checked = false);
    }

    loadDrafts() {
        const drafts = JSON.parse(localStorage.getItem('content-drafts') || '[]');
        const list = document.getElementById('drafts-list');

        if (drafts.length === 0) {
            list.innerHTML = '<p class="loading">No drafts yet</p>';
            return;
        }

        list.innerHTML = '';
        drafts.forEach(draft => {
            const card = document.createElement('div');
            card.className = 'draft-card';
            card.innerHTML = `
                <div class="draft-info">
                    <h4>${this.escapeHtml(draft.campaign)}</h4>
                    <p>Created: ${draft.created}</p>
                </div>
                <div class="draft-actions">
                    <button class="btn" onclick="dashboard.editDraft(${draft.id})">✏️ Edit</button>
                    <button class="btn btn-danger" onclick="dashboard.deleteDraft(${draft.id})">🗑️ Delete</button>
                </div>
            `;
            list.appendChild(card);
        });
    }

    editDraft(id) {
        const drafts = JSON.parse(localStorage.getItem('content-drafts') || '[]');
        const draft = drafts.find(d => d.id === id);
        if (draft) {
            document.getElementById('creator-campaign-name').value = draft.campaign;
            document.getElementById('creator-content').value = draft.content;
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelector('[data-tab="content-creator"]').classList.add('active');
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.getElementById('content-creator-tab').classList.add('active');
        }
    }

    deleteDraft(id) {
        if (!confirm('Delete this draft?')) return;
        let drafts = JSON.parse(localStorage.getItem('content-drafts') || '[]');
        drafts = drafts.filter(d => d.id !== id);
        localStorage.setItem('content-drafts', JSON.stringify(drafts));
        this.loadDrafts();
    }

    escapeHtml(text) {
        const map = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'};
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    startAutoRefresh() {
        // Load drafts initially
        this.loadDrafts();

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
