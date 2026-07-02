<script setup>
import { inject } from 'vue'

defineProps({
  shortCode: {
    type: String,
    required: true
  },
  shortUrl: {
    type: String,
    required: true
  }
})

const getQrUrl = inject('getQrUrl')
</script>

<template>
  <div class="qr-content">
    <img :src="getQrUrl(shortCode)" alt="QR Code" class="qr-image" />
    <div class="qr-details">
      <slot>
        <h4>Scan to visit</h4>
        <p>Scan this code to immediately open the shortened URL.</p>
      </slot>
      <a :href="getQrUrl(shortCode)" download="qrcode.png" target="_blank" class="qr-download-link">
        Download PNG
      </a>
    </div>
  </div>
</template>

<style scoped>
.qr-content {
  display: flex;
  align-items: center;
  gap: 24px;
  text-align: left;
}

@media (max-width: 480px) {
  .qr-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}

.qr-image {
  width: 140px;
  height: 140px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px;
  background-color: #FFFFFF;
}

.qr-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.qr-details h4 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-top: 0;
  margin-bottom: 0;
}

.qr-details p {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 0;
  margin-bottom: 0;
}

.qr-download-link {
  display: inline-block;
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  color: #374151;
  font-size: 13px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 6px;
  align-self: flex-start;
  transition: all 0.2s;
}

@media (max-width: 480px) {
  .qr-download-link {
    align-self: center;
  }
}

.qr-download-link:hover {
  background-color: #F9FAFB;
  border-color: #D1D5DB;
}
</style>
