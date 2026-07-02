<script setup>
import QrCodeCard from './QrCodeCard.vue'
import StatsCard from './StatsCard.vue'

defineProps({
  links: {
    type: Array,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  activeQrCode: {
    type: String,
    default: null
  },
  activeStats: {
    type: Object,
    default: null
  },
  timeAgo: {
    type: Function,
    required: true
  }
})

defineEmits(['toggleQr', 'toggleStats', 'copy', 'refresh'])
</script>

<template>
  <section class="recent-section">
    <div class="recent-header">
      <h2 class="section-title">Recent Links</h2>
      <a href="#" class="view-all-link" @click.prevent="$emit('refresh')">Refresh table &rarr;</a>
    </div>

    <div class="table-container">
      <table class="recent-table">
        <thead>
          <tr>
            <th class="th-left">Short Link</th>
            <th class="th-left">Destination</th>
            <th class="th-center">Clicks</th>
            <th class="th-left">Created</th>
            <th class="th-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <!-- Loading Skeleton State -->
          <template v-if="isLoading">
            <tr v-for="i in 3" :key="'skeleton-'+i">
              <td><div class="skeleton skeleton-text" style="width: 140px; height: 16px;"></div></td>
              <td><div class="skeleton skeleton-text" style="width: 250px; height: 16px;"></div></td>
              <td><div class="skeleton skeleton-text" style="width: 40px; height: 16px; margin: 0 auto;"></div></td>
              <td><div class="skeleton skeleton-text" style="width: 100px; height: 16px;"></div></td>
              <td><div class="skeleton skeleton-text" style="width: 80px; height: 16px; margin: 0 auto;"></div></td>
            </tr>
          </template>

          <!-- Empty State -->
          <tr v-else-if="links.length === 0">
            <td colspan="5" class="empty-state">
              <div class="empty-state-content">
                <svg viewBox="0 0 20 20" fill="currentColor" width="36" height="36" class="empty-icon">
                  <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"/>
                </svg>
                <p>No links yet. Create your first short link above.</p>
              </div>
            </td>
          </tr>

          <!-- Data Rows -->
          <template v-else>
            <template v-for="link in links" :key="link.short_code">
              <tr class="table-row">
                <td>
                  <a :href="link.short_url" target="_blank" class="table-short-link">
                    {{ link.short_url }}
                  </a>
                </td>
                <td>
                  <div class="table-long-url" :title="link.long_url">
                    {{ link.long_url }}
                  </div>
                </td>
                <td class="td-center clicks-count">
                  {{ link.click_count }}
                </td>
                <td class="created-time">
                  {{ timeAgo(link.created_at) }}
                </td>
                <td>
                  <div class="action-icons">
                    <button class="icon-btn" title="View Stats" @click="$emit('toggleStats', link.short_code)" :class="{ 'icon-active': activeStats && activeStats.short_code === link.short_code }">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                        <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/>
                      </svg>
                    </button>
                    <button class="icon-btn" title="QR Code" @click="$emit('toggleQr', link.short_code)" :class="{ 'icon-active': activeQrCode === link.short_code }">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                        <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm2 2V5h1v1H5zm3 4a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 01-1 1H9a1 1 0 01-1-1v-3zm2 2v-1h1v1h-1zM3 12a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 01-1 1H4a1 1 0 01-1-1v-3zm2 2v-1h1v1H5zm10-7h-2V5h2v2zm0 5h-2v2h2v-2z" clip-rule="evenodd"/>
                        <path d="M13 10h2v1h-2v-1zM11 15h1v1h-1v-1zM13 14h1v1h-1v-1zM10 14h1v1h-1v-1zM12 11h1v1h-1v-1zM14 13h1v1h-1v-1zM15 16h1v1h-1v-1zM16 14h1v1h-1v-1zM16 11h1v1h-1v-1zM15 12h1v1h-1v-1zM12 13h1v1h-1v-1z"/>
                      </svg>
                    </button>
                    <button class="icon-btn btn-dot" title="Options" @click="$emit('copy', link.short_url)">
                      <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                        <path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM18 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>

              <!-- Expandable Row for QR Code in Table -->
              <tr v-if="activeQrCode === link.short_code" :key="'qr-'+link.short_code">
                <td colspan="5" class="table-expand-cell">
                  <div class="expand-wrapper">
                    <QrCodeCard :short-code="link.short_code" :short-url="link.short_url">
                      <h4>QR Code for {{ link.short_code }}</h4>
                      <p>Scan this code to immediately open the shortened URL: <a :href="link.short_url" target="_blank">{{ link.short_url }}</a></p>
                    </QrCodeCard>
                  </div>
                </td>
              </tr>

              <!-- Expandable Row for Stats in Table -->
              <tr v-if="activeStats && activeStats.short_code === link.short_code" :key="'stats-'+link.short_code">
                <td colspan="5" class="table-expand-cell">
                  <div class="expand-wrapper">
                    <StatsCard :stats="activeStats" :show-header="false" />
                  </div>
                </td>
              </tr>
            </template>
          </template>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.recent-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
  width: 100%;
}

.recent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.view-all-link {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-color);
}

.view-all-link:hover {
  text-decoration: underline;
}

.table-container {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  box-shadow: var(--shadow-card);
  width: 100%;
}

.recent-table {
  width: 100%;
  border-collapse: collapse;
}

.recent-table th {
  background-color: #F9FAFB;
  font-size: 12px;
  font-weight: 600;
  color: #4B5563;
  padding: 12px 18px;
  border-bottom: 1px solid var(--border-color);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.th-left {
  text-align: left;
}

.th-center {
  text-align: center;
}

.recent-table td {
  padding: 16px 18px;
  font-size: 14px;
  color: #374151;
  border-bottom: 1px solid var(--border-color);
}

.table-row:hover {
  background-color: #FAFBFD;
}

.table-short-link {
  font-family: var(--mono-sans);
  color: var(--primary-color);
  font-weight: 600;
}

.table-short-link:hover {
  text-decoration: underline;
}

.table-long-url {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text-secondary);
}

.td-center {
  text-align: center;
}

.clicks-count {
  font-weight: 500;
  color: var(--text-primary);
}

.created-time {
  color: var(--text-secondary);
}

.action-icons {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.icon-btn {
  background: none;
  border: none;
  color: #9CA3AF;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  color: var(--text-primary);
  background-color: #F3F4F6;
}

.icon-active {
  color: var(--primary-color);
  background-color: #EEF2FF;
}

/* TABLE EXPAND ROW */
.table-expand-cell {
  background-color: #F9FAFB;
  border-bottom: 1px solid var(--border-color);
  padding: 0 !important;
}

.expand-wrapper {
  padding: 20px;
  border-bottom: 1.5px dashed var(--border-color);
}

/* EMPTY STATE */
.empty-state {
  padding: 48px 18px !important;
  text-align: center;
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.empty-icon {
  color: #D1D5DB;
}

.empty-state p {
  color: var(--text-secondary);
  font-size: 15px;
}

/* SKELETON */
.skeleton-text {
  border-radius: 4px;
}
</style>
