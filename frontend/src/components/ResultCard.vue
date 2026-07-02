<script setup>
defineProps({
  result: {
    type: Object,
    required: true
  },
  copySuccess: {
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
  }
})

defineEmits(['copy', 'toggleQr', 'toggleStats'])
</script>

<template>
  <div class="result-card">
    <div class="result-left">
      <div class="check-icon-circle">
        <svg viewBox="0 0 20 20" fill="currentColor" width="20" height="20">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
        </svg>
      </div>
      <div class="result-info">
        <span class="result-status">Your short link is ready!</span>
        <a :href="result.short_url" target="_blank" class="short-url-link">{{ result.short_url }}</a>
      </div>
    </div>
    <div class="result-right">
      <button @click="$emit('copy')" class="action-btn">
        {{ copySuccess ? 'Copied!' : 'Copy' }}
      </button>
      <button @click="$emit('toggleQr', result.short_code)" class="action-btn" :class="{ 'btn-active': activeQrCode === result.short_code }">
        QR Code
      </button>
      <button @click="$emit('toggleStats', result.short_code)" class="action-btn" :class="{ 'btn-active': activeStats && activeStats.short_code === result.short_code }">
        View stats
      </button>
    </div>
  </div>
</template>

<style scoped>
.result-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: var(--shadow-card);
  gap: 24px;
}

@media (max-width: 768px) {
  .result-card {
    flex-direction: column;
    align-items: flex-start;
    padding: 24px;
  }
}

.result-left {
  display: flex;
  align-items: center;
  gap: 16px;
  text-align: left;
}

.check-icon-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #D1FAE5;
  color: #059669;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.result-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.result-status {
  font-size: 13px;
  font-weight: 600;
  color: #059669;
}

.short-url-link {
  font-family: var(--mono-sans);
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color);
  word-break: break-all;
}

.short-url-link:hover {
  text-decoration: underline;
}

.result-right {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .result-right {
    width: 100%;
  }
}

.action-btn {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  color: #374151;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background-color: #F9FAFB;
  border-color: #D1D5DB;
}

.btn-active {
  background-color: #EEF2FF;
  border-color: #C7D2FE;
  color: var(--primary-color);
}
</style>
