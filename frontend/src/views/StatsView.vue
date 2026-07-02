<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Download, MousePointerClick, Calendar, Clock, ExternalLink } from 'lucide-vue-next'
import { getStats, getQrUrl } from '../api/shortener.js'

const route = useRoute()
const router = useRouter()
const shortCode = route.params.shortCode

const stats = ref(null)
const isLoading = ref(true)
const error = ref(null)
const isDownloading = ref(false)

// Function to format date to DD MMM YYYY (e.g. 02 Jul 2026)
function formatDate(dateString) {
  if (!dateString) return '-'
  
  // Normalize date string for Safari / cross-browser consistency (make naive UTC)
  let normalized = dateString
  if (!dateString.endsWith('Z') && !dateString.includes('+') && !dateString.includes('-T')) {
    if (!/[\+\-]\d{2}:?\d{2}$/.test(dateString)) {
      normalized = dateString + 'Z'
    }
  }
  
  const date = new Date(normalized)
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

// Function to check if the link is expired
function checkExpiry() {
  if (!stats.value) return { status: 'active', text: 'Active' }
  if (stats.value.is_expired) {
    return { status: 'expired', text: 'Expired' }
  }
  if (stats.value.expires_at) {
    return { status: 'expires', text: `Expires ${formatDate(stats.value.expires_at)}` }
  }
  return { status: 'active', text: 'Active' }
}

async function fetchStats() {
  isLoading.value = true
  error.value = null
  try {
    const data = await getStats(shortCode)
    stats.value = data
  } catch (err) {
    console.error('Error fetching stats:', err)
    if (err.response && err.response.status === 404) {
      error.value = 'not_found'
    } else {
      error.value = 'failed'
    }
  } finally {
    isLoading.value = false
  }
}

async function downloadQr() {
  if (isDownloading.value) return
  isDownloading.value = true
  try {
    const url = getQrUrl(shortCode)
    const response = await fetch(url)
    const blob = await response.blob()
    const blobUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = blobUrl
    link.download = `qr-${shortCode}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(blobUrl)
  } catch (err) {
    console.error('Failed to download QR code:', err)
    alert('Failed to download QR code. Please try again.')
  } finally {
    isDownloading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<template>
  <div class="stats-container">
    <!-- Header Navbar -->
    <header class="stats-header-nav">
      <div class="nav-content">
        <span class="logo" @click="router.push('/')">Shrinkr<span class="indigo-dot">.</span></span>
      </div>
    </header>

    <div class="stats-content-wrapper">
      <!-- Back Button -->
      <button @click="router.push('/')" class="back-btn">
        <ArrowLeft :size="16" />
        <span>Back</span>
      </button>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading performance statistics...</p>
      </div>

      <!-- Error State (404: Not Found) -->
      <div v-else-if="error === 'not_found'" class="error-card">
        <div class="error-icon-wrapper">
          <span class="error-emoji">🔍</span>
        </div>
        <h2>Link not found</h2>
        <p>The short URL /{{ shortCode }} does not exist in our database or has been deleted.</p>
        <button @click="router.push('/')" class="home-btn">
          Back to Home
        </button>
      </div>

      <!-- Error State (Other errors) -->
      <div v-else-if="error" class="error-card">
        <div class="error-icon-wrapper">
          <span class="error-emoji">⚠️</span>
        </div>
        <h2>Something went wrong</h2>
        <p>Failed to load statistics for this short link. Please check your network and try again.</p>
        <button @click="router.push('/')" class="home-btn">
          Back to Home
        </button>
      </div>

      <!-- Main Stats Layout -->
      <div v-else-if="stats" class="stats-layout">
        <!-- Title & Subtitle -->
        <div class="link-info-header">
          <h1 class="short-code-title">/{{ stats.short_code }}</h1>
          <div class="original-url-wrapper">
            <span class="original-url-label">Original URL:</span>
            <a :href="stats.long_url" target="_blank" class="original-url-link" :title="stats.long_url">
              {{ stats.long_url }}
              <ExternalLink :size="12" class="link-icon" />
            </a>
          </div>
        </div>

        <!-- 3-Column Grid -->
        <div class="stats-grid">
          <!-- Total Clicks -->
          <div class="stat-card">
            <div class="card-icon-wrapper clicks-bg">
              <MousePointerClick :size="20" class="card-icon indigo" />
            </div>
            <div class="card-body">
              <span class="stat-value">{{ stats.click_count }}</span>
              <span class="stat-label">Total Clicks</span>
            </div>
          </div>

          <!-- Created Date -->
          <div class="stat-card">
            <div class="card-icon-wrapper created-bg">
              <Calendar :size="20" class="card-icon gray" />
            </div>
            <div class="card-body">
              <span class="stat-value date-val">{{ formatDate(stats.created_at) }}</span>
              <span class="stat-label">Created</span>
            </div>
          </div>

          <!-- Expiry Status -->
          <div class="stat-card">
            <div class="card-icon-wrapper status-bg">
              <Clock :size="20" class="card-icon status-icon" />
            </div>
            <div class="card-body">
              <!-- If expired: badge merah -->
              <div v-if="checkExpiry().status === 'expired'">
                <span class="badge badge-expired">Expired</span>
              </div>
              <!-- If active and no expiry: badge hijau -->
              <div v-else-if="checkExpiry().status === 'active'">
                <span class="badge badge-active">Active</span>
              </div>
              <!-- If active with expiry: text Expires [date] -->
              <div v-else-if="checkExpiry().status === 'expires'">
                <span class="expiry-text-value">{{ checkExpiry().text }}</span>
              </div>
              <span class="stat-label">Status</span>
            </div>
          </div>
        </div>

        <!-- QR Code Card -->
        <div class="qr-code-card">
          <div class="qr-card-header">
            <h3>QR Code</h3>
            <p>Scan or share this code to direct users to the shortened URL.</p>
          </div>
          <div class="qr-card-body">
            <div class="qr-wrapper">
              <img :src="getQrUrl(stats.short_code)" alt="QR Code" class="qr-image" />
            </div>
            <button @click="downloadQr" class="download-btn" :disabled="isDownloading">
              <Download :size="16" />
              <span>{{ isDownloading ? 'Downloading...' : 'Download QR' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

.stats-header-nav {
  background-color: #FFFFFF;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.5px;
  cursor: pointer;
}

.indigo-dot {
  color: var(--primary-color);
}

.stats-content-wrapper {
  flex: 1;
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Back button */
.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  align-self: flex-start;
  padding: 6px 12px;
  margin-left: -12px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.back-btn:hover {
  color: var(--text-primary);
  background-color: rgba(0, 0, 0, 0.04);
}

/* Loading & Error States */
.loading-state, .error-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 48px 32px;
  text-align: center;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(99, 102, 241, 0.1);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s infinite linear;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-emoji {
  font-size: 48px;
}

.error-card h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.error-card p {
  color: var(--text-secondary);
  max-width: 400px;
  font-size: 15px;
}

.home-btn {
  background-color: var(--primary-color);
  color: #FFFFFF;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 8px;
}

.home-btn:hover {
  background-color: var(--primary-hover);
}

/* Link Info Header */
.link-info-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 8px;
}

.short-code-title {
  font-family: var(--mono-sans);
  color: var(--primary-color);
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -1px;
}

.original-url-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.original-url-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

.original-url-link {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 400;
  text-decoration: underline;
  text-underline-offset: 3px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  max-width: 500px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.2s ease;
}

.original-url-link:hover {
  color: var(--primary-color);
}

.link-icon {
  flex-shrink: 0;
  opacity: 0.7;
}

/* Grid layout for stats cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.card-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.clicks-bg {
  background-color: rgba(99, 102, 241, 0.08);
}

.created-bg {
  background-color: rgba(107, 114, 128, 0.08);
}

.status-bg {
  background-color: rgba(16, 185, 129, 0.08);
}

.card-icon.indigo {
  color: var(--primary-color);
}

.card-icon.gray {
  color: var(--text-secondary);
}

.card-icon.status-icon {
  color: #10B981;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.date-val {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.2px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Expiry statuses */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 600;
  line-height: 1;
}

.badge-active {
  background-color: #DEF7EC;
  color: #03543F;
}

.badge-expired {
  background-color: #FDE8E8;
  color: #9B1C1C;
}

.expiry-text-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

/* QR Code Card */
.qr-code-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-card);
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.qr-card-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.qr-card-header p {
  font-size: 14px;
  color: var(--text-secondary);
}

.qr-card-body {
  display: flex;
  align-items: center;
  gap: 32px;
}

.qr-wrapper {
  background-color: #F9FAFB;
  border: 1px dashed var(--border-color);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.qr-image {
  width: 140px;
  height: 140px;
  display: block;
}

.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: var(--primary-color);
  color: #FFFFFF;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.download-btn:hover:not(:disabled) {
  background-color: var(--primary-hover);
}

.download-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Media Queries for responsiveness */
@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .qr-card-body {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 20px;
  }
  
  .original-url-link {
    max-width: 100%;
  }
  
  .short-code-title {
    font-size: 28px;
  }
}
</style>
