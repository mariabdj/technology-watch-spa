document.addEventListener('alpine:init', () => {
    Alpine.data('dashboard', () => ({
        // --- ETAT ---
        currentTab: 'dashboard',
        sidebarOpen: false,
        isDark: true,
        loading: false, 
        isScanning: false, 
        scanProgress: 0,
        hasNewData: false,
        showGlossary: false,
        selectedItem: null,
        
        // Timestamps
        timestamps: { lastScan: '--:--', lastArticle: '--:--' },

        // Données
        news: [],
        stats: {},
        filters: { search: '', provider: 'all', impact: 'all', category: 'all' },
        chatInput: '', chatLoading: false, chatMessages: [],
        navItems: [ { id: 'dashboard', label: 'Dashboard', icon: 'ri-layout-grid-line' }, { id: 'saved', label: 'Sauvegardes', icon: 'ri-bookmark-3-line' }, { id: 'analytics', label: 'Analyses', icon: 'ri-bar-chart-box-line' }, { id: 'suggestions', label: 'Advisor IA', icon: 'ri-magic-line' } ],

        init() {
            if(window.innerWidth >= 768) this.sidebarOpen = true;
            if (localStorage.getItem('theme') === 'light') {
                this.isDark = false;
                document.documentElement.classList.remove('dark');
            }
            
            // Chargement Initial
            this.refreshData();
            
            // Check Scan Status
            this.checkScanStatus();
        },

        switchTab(id) {
            this.currentTab = id;
            if(window.innerWidth < 768) this.sidebarOpen = false;
            if(id === 'analytics') setTimeout(() => this.initCharts(), 100);
        },

        // --- DATA & TIMESTAMPS ---
        async refreshData() {
            this.loading = true;
            this.hasNewData = false;
            await this.fetchData();
            await this.fetchStats();
            await this.updateTimestamps();
            this.loading = false;
        },

        async fetchData() {
            try {
                const res = await fetch('http://127.0.0.1:8000/news');
                this.news = await res.json();
            } catch (e) { console.error(e); }
        },

        async fetchStats() {
            try {
                const res = await fetch('http://127.0.0.1:8000/stats');
                this.stats = await res.json();
            } catch (e) { console.error(e); }
        },

        async updateTimestamps() {
            // CORRECTION MAJEURE: Force le fuseau horaire Algérie pour l'affichage
            const timeOptions = { timeZone: 'Africa/Algiers', hour: '2-digit', minute: '2-digit' };
            const dateOptions = { timeZone: 'Africa/Algiers', day: 'numeric', month: 'short' };

            try {
                // 1. Last Scan Time
                const res = await fetch('http://127.0.0.1:8000/scan-status');
                const state = await res.json();
                
                if(state.last_execution) {
                    const dateScan = new Date(state.last_execution);
                    this.timestamps.lastScan = new Intl.DateTimeFormat('fr-FR', timeOptions).format(dateScan);
                }

                // 2. Last Article Time
                if(this.news && this.news.length > 0) {
                    // On prend la date de création de l'article le plus récent
                    const dateArt = new Date(this.news[0].created_at);
                    
                    const day = new Intl.DateTimeFormat('fr-FR', dateOptions).format(dateArt);
                    const time = new Intl.DateTimeFormat('fr-FR', timeOptions).format(dateArt);
                    
                    this.timestamps.lastArticle = `${day} ${time}`;
                }
            } catch(e) {}
        },

        // --- SCAN LOGIC ---
        async triggerScan() {
            if (this.isScanning) return;
            try {
                const res = await fetch('http://127.0.0.1:8000/trigger-scan', { method: 'POST' });
                const data = await res.json();
                if(data.status === 'started') {
                    this.isScanning = true;
                    this.monitorScanProgress();
                }
            } catch (e) { console.error(e); }
        },

        async checkScanStatus() {
            const timeOptions = { timeZone: 'Africa/Algiers', hour: '2-digit', minute: '2-digit' };
            try {
                const res = await fetch('http://127.0.0.1:8000/scan-status');
                const state = await res.json();
                if(state.is_scanning) {
                    this.isScanning = true;
                    this.monitorScanProgress();
                } else {
                    if(state.last_execution) {
                        const dateScan = new Date(state.last_execution);
                        this.timestamps.lastScan = new Intl.DateTimeFormat('fr-FR', timeOptions).format(dateScan);
                    }
                }
            } catch(e) {}
        },

        monitorScanProgress() {
            const interval = setInterval(async () => {
                if(!this.isScanning) {
                    clearInterval(interval);
                    return;
                }
                try {
                    const res = await fetch('http://127.0.0.1:8000/scan-status');
                    const state = await res.json();
                    
                    this.scanProgress = state.progress;
                    this.isScanning = state.is_scanning;

                    if (!state.is_scanning) {
                        clearInterval(interval);
                        if (state.new_added > 0) this.hasNewData = true;
                        this.refreshData(); // Refresh auto à la fin
                    }
                } catch(e) {
                    clearInterval(interval);
                    this.isScanning = false;
                }
            }, 1000);
        },

        // --- FILTERS & COMPUTED ---
        get uniqueCategories() {
            if(!this.news) return [];
            const cats = this.news.map(n => n.category).filter(c => c);
            return [...new Set(cats)];
        },

        async toggleSave(item) {
            if(!item) return;
            item.is_saved = !item.is_saved;
            try { await fetch(`http://127.0.0.1:8000/news/${item.id}/toggle-save`, { method: 'POST' }); } 
            catch(e) { item.is_saved = !item.is_saved; }
        },

        get savedNews() { if(!this.news) return []; return this.news.filter(n => n.is_saved); },

        get filteredNews() {
            if (!this.news) return [];
            return this.news.filter(item => {
                const matchProv = this.filters.provider === 'all' || item.provider === this.filters.provider;
                const matchImp = this.filters.impact === 'all' || item.impact_level == this.filters.impact;
                const matchCat = this.filters.category === 'all' || item.category === this.filters.category;
                const search = this.filters.search.toLowerCase();
                const matchSearch = !search || item.title.toLowerCase().includes(search) || item.summary.toLowerCase().includes(search);
                return matchProv && matchImp && matchCat && matchSearch;
            });
        },
        
        resetFilters() { this.filters = { search: '', provider: 'all', impact: 'all', category: 'all' }; },
        toggleTheme() {
            this.isDark = !this.isDark;
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', this.isDark ? 'dark' : 'light');
            if(this.currentTab === 'analytics') this.initCharts();
        },
        openModal(item) { this.selectedItem = item; },
        
        getProviderClass(p) { if(p==='AWS') return 'bg-orange-100 text-orange-600 dark:bg-orange-500/10 dark:text-orange-500'; if(p==='Azure') return 'bg-blue-100 text-blue-600 dark:bg-blue-500/10 dark:text-blue-500'; return 'bg-red-100 text-red-600 dark:bg-red-500/10 dark:text-red-500'; },
        getProviderIcon(p) { if(p==='AWS') return 'ri-amazon-fill'; if(p==='Azure') return 'ri-microsoft-fill'; return 'ri-google-fill'; },
        getImpactClass(l) { if(l===3) return 'bg-red-50 text-red-600 border-red-100 dark:bg-red-500/10 dark:text-red-400 dark:border-red-500/20'; if(l===2) return 'bg-yellow-50 text-yellow-600 border-yellow-100 dark:bg-yellow-500/10 dark:text-yellow-400 dark:border-yellow-500/20'; return 'bg-gray-50 text-gray-600 border-gray-100 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700'; },
        getImpactLabel(l) { return l===3 ? 'Critique' : (l===2 ? 'Majeur' : 'Mineur'); },

        async sendMessage() {
            if (!this.chatInput.trim()) return;
            const userMsg = this.chatInput;
            this.chatMessages.push({ role: 'user', content: userMsg });
            this.chatInput = '';
            this.chatLoading = true;
            setTimeout(() => { document.getElementById('chatContainer').scrollTop = 9999; }, 100);
            try {
                const res = await fetch('http://127.0.0.1:8000/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ question: userMsg }) });
                const data = await res.json();
                this.chatMessages.push({ role: 'bot', content: marked.parse(data.response) });
            } catch (e) { this.chatMessages.push({ role: 'bot', content: "Erreur IA." }); } 
            finally { this.chatLoading = false; setTimeout(() => { document.getElementById('chatContainer').scrollTop = 9999; }, 100); }
        },
        autoGenerateAdvice() { this.chatInput = "Génère un rapport stratégique rapide."; this.sendMessage(); },

        initCharts() {
            if(!this.stats.providers_stats) return;
            const textColor = this.isDark ? '#e5e7eb' : '#374151';
            ['providerChart', 'categoryChart', 'timelineChart'].forEach(id => { const el = document.getElementById(id); if(el && Chart.getChart(el)) Chart.getChart(el).destroy(); });
            new Chart(document.getElementById('providerChart'), { type: 'doughnut', data: { labels: Object.keys(this.stats.providers_stats), datasets: [{ data: Object.values(this.stats.providers_stats), backgroundColor: ['#f97316', '#3b82f6', '#ef4444'], borderWidth: 0 }] }, options: { maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: textColor } } } } });
            new Chart(document.getElementById('categoryChart'), { type: 'bar', data: { labels: Object.keys(this.stats.categories_stats), datasets: [{ label: 'Articles', data: Object.values(this.stats.categories_stats), backgroundColor: '#8b5cf6', borderRadius: 5 }] }, options: { maintainAspectRatio: false, scales: { y: { ticks: { color: textColor } }, x: { ticks: { color: textColor } } }, plugins: { legend: { display: false } } } });
            const sortedDates = Object.keys(this.stats.timeline_stats).sort();
            new Chart(document.getElementById('timelineChart'), { type: 'line', data: { labels: sortedDates, datasets: [{ label: 'Volume', data: sortedDates.map(d => this.stats.timeline_stats[d]), borderColor: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.1)', fill: true, tension: 0.4 }] }, options: { maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { color: textColor } }, x: { ticks: { color: textColor } } }, plugins: { legend: { display: false } } } });
        }
    }));
});