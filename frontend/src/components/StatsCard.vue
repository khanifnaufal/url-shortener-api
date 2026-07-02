<script setup>
defineProps({
  stats: {
    type: Object,
    required: true
  },
  showHeader: {
    type: Boolean,
    default: true
  }
})
</script>

<template>
  <div v-if="stats" class="inline-stats-card" :class="{ 'compact': !showHeader }">
    <div v-if="showHeader" class="stats-header">
      <h4>Link Performance</h4>
    </div>
    <div class="stats-grid">
      <div class="stats-item">
        <span class="stats-label">Total Clicks</span>
        <span class="stats-val">{{ stats.click_count }}</span>
      </div>
      <div class="stats-item">
        <span class="stats-label">Created At</span>
        <span class="stats-val">{{ new Date(stats.created_at).toLocaleString() }}</span>
      </div>
      <div class="stats-item">
        <span class="stats-label">Expires At</span>
        <span class="stats-val">{{ stats.expires_at ? new Date(stats.expires_at).toLocaleString() : 'No expiry' }}</span>
      </div>
      <div class="stats-item">
        <span class="stats-label">Status</span>
        <span class="status-badge" :class="stats.is_expired ? 'badge-expired' : 'badge-active'">
          {{ stats.is_expired ? 'Expired' : 'Active' }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.inline-stats-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-card);
  text-align: left;
}

.inline-stats-card.compact {
  margin-top: 0;
  box-shadow: none;
  border: none;
  padding: 12px 16px;
}

.stats-header {
  margin-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 8px;
}

.stats-header h4 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-top: 0;
  margin-bottom: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
}

.stats-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background-color: #F9FAFB;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.stats-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
}

.stats-val {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.status-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 9999px;
  align-self: flex-start;
}

.badge-active {
  background-color: #D1FAE5;
  color: #065F46;
}

.badge-expired {
  background-color: #FEE2E2;
  color: #991B1B;
}
</style>
