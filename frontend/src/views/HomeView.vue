<script setup>
import { ref, onMounted } from 'vue'
import { Github, ExternalLink, Zap, BarChart2, QrCode, Timer, ShieldCheck, Link, Server, Gauge, Layers, Heart, ArrowRight } from 'lucide-vue-next'
import { shortenUrl, getUrls, getStats, getQrUrl } from '../api/shortener.js'

// API base URL for Swagger docs
const apiDocsUrl = import.meta.env.VITE_API_BASE_URL + '/docs'

// Form state
const longUrl = ref('')
const customAlias = ref('')
const expiresIn = ref('null') // stores string representation: 'null', '1', '24', '168'

// App state
const result = ref(null)
const recentLinks = ref([])
const isLoading = ref(false)
const isLoadingRecent = ref(false)
const error = ref(null)
const inlineValidationError = ref('')

// Interactive features state
const activeQrCode = ref(null) // holds short_code of currently visible QR
const activeStats = ref(null) // holds stats object of currently visible stats code
const isLoadingStats = ref(false)
const copySuccess = ref(false)

// Helper to calculate time ago
function timeAgo(dateString) {
  if (!dateString) return ''
  // Append Z to treat naive database timestamps as UTC
  let normalizedDate = dateString
  if (!dateString.endsWith('Z') && !dateString.includes('+') && !dateString.includes('-T')) {
    // A regex check to ensure no timezone offset is already present
    if (!/[\+\-]\d{2}:?\d{2}$/.test(dateString)) {
      normalizedDate = dateString + 'Z'
    }
  }
  const date = new Date(normalizedDate)
  const now = new Date()
  const diffMs = Math.max(0, now.getTime() - date.getTime())
  
  const seconds = Math.floor(diffMs / 1000)
  if (seconds < 60) {
    return 'Just now'
  }
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) {
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
  }
  const hours = Math.floor(minutes / 60)
  if (hours < 24) {
    return `${hours} hour${hours > 1 ? 's' : ''} ago`
  }
  const days = Math.floor(hours / 24)
  if (days < 30) {
    return `${days} day${days > 1 ? 's' : ''} ago`
  }
  const months = Math.floor(days / 30)
  return `${months} month${months > 1 ? 's' : ''} ago`
}

// Fetch recent links
async function fetchRecentLinks() {
  isLoadingRecent.value = true
  try {
    const data = await getUrls()
    recentLinks.value = data
  } catch (err) {
    console.error('Failed to fetch recent links:', err)
  } finally {
    isLoadingRecent.value = false
  }
}

// Handle Shorten submission
async function handleShorten() {
  error.value = null
  inlineValidationError.value = ''
  
  // Validate longUrl is not empty
  if (!longUrl.value.trim()) {
    inlineValidationError.value = 'Please enter a long URL.'
    return
  }

  // Basic URL format validation
  try {
    new URL(longUrl.value)
  } catch (_) {
    inlineValidationError.value = 'Please enter a valid URL (e.g. https://google.com).'
    return
  }

  isLoading.value = true
  result.value = null
  activeQrCode.value = null
  activeStats.value = null
  
  // Map expiresIn dropdown string value to numeric hours or null
  let hours = null
  if (expiresIn.value !== 'null') {
    hours = parseInt(expiresIn.value, 10)
  }

  try {
    const data = await shortenUrl(
      longUrl.value.trim(),
      customAlias.value.trim() || null,
      hours
    )
    result.value = data
    
    // Clear form inputs except expiresIn
    longUrl.value = ''
    customAlias.value = ''
    
    // Refresh table
    await fetchRecentLinks()
  } catch (err) {
    // Extract error message from API response
    if (err.response && err.response.data && err.response.data.detail) {
      if (Array.isArray(err.response.data.detail)) {
        error.value = err.response.data.detail[0]?.msg || 'Failed to shorten URL.'
      } else {
        error.value = err.response.data.detail
      }
    } else {
      error.value = 'An error occurred while connecting to the server.'
    }
  } finally {
    isLoading.value = false
  }
}

// Copy URL to clipboard
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text)
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy to clipboard', err)
  }
}

// Toggle QR Code visibility
function toggleQr(shortCode) {
  if (activeQrCode.value === shortCode) {
    activeQrCode.value = null
  } else {
    activeQrCode.value = shortCode
    activeStats.value = null // close stats if open
  }
}

// Toggle and fetch URL stats
async function toggleStats(shortCode) {
  if (activeStats.value && activeStats.value.short_code === shortCode) {
    activeStats.value = null
    return
  }
  
  isLoadingStats.value = true
  activeQrCode.value = null // close QR if open
  
  try {
    const statsData = await getStats(shortCode)
    activeStats.value = statsData
  } catch (err) {
    console.error('Failed to fetch stats:', err)
    alert('Failed to load stats. Please try again.')
  } finally {
    isLoadingStats.value = false
  }
}

function scrollToFeatures() {
  const el = document.getElementById('features')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

function scrollToAbout() {
  const el = document.getElementById('about')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(() => {
  fetchRecentLinks()
})
</script>

<template>
  <div class="home-container">
    <!-- NAVBAR -->
    <nav class="navbar">
      <div class="nav-content">
        <div class="nav-left">
          <span class="logo">Shrinkr<span class="indigo-dot">.</span></span>
        </div>
        <div class="nav-right">
          <div class="nav-links">
            <a href="#" class="nav-link" @click.prevent="scrollToAbout">About</a>
            <a href="#" class="nav-link" @click.prevent="scrollToFeatures">Features</a>
            <a :href="apiDocsUrl" target="_blank" rel="noopener noreferrer" class="nav-link api-link">
              API
              <ExternalLink size="14" class="nav-icon-right" />
            </a>
          </div>
          <a href="https://github.com/khanifnaufal/url-shortener-api" target="_blank" rel="noopener noreferrer" class="github-btn">
            <Github size="16" />
            GitHub
          </a>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <!-- HERO & FORM SECTION -->
      <section class="hero-section">
        <!-- Left Hero Text -->
        <div class="hero-left">
          <h1 class="hero-heading">Shorten links,<br>share anywhere.</h1>
          <p class="hero-subtext">Paste a long URL and get a short link instantly.<br>Fast. Simple. Reliable.</p>
        </div>

        <!-- Right Form Card -->
        <div class="hero-right">
          <div class="form-card">
            <form @submit.prevent="handleShorten">
              <div class="form-group">
                <label for="longUrl" class="form-label">Your long URL</label>
                <input
                  id="longUrl"
                  v-model="longUrl"
                  type="text"
                  class="form-input"
                  :class="{ 'input-error': inlineValidationError }"
                  placeholder="https://..."
                  :disabled="isLoading"
                />
                <span v-if="inlineValidationError" class="error-text">{{ inlineValidationError }}</span>
              </div>

              <div class="form-row">
                <div class="form-group col-half">
                  <label for="customAlias" class="form-label">Custom alias (optional)</label>
                  <input
                    id="customAlias"
                    v-model="customAlias"
                    type="text"
                    class="form-input"
                    placeholder="e.g. my-link"
                    :disabled="isLoading"
                  />
                </div>
                <div class="form-group col-half">
                  <label for="expiresIn" class="form-label">Expires in</label>
                  <select
                    id="expiresIn"
                    v-model="expiresIn"
                    class="form-select"
                    :disabled="isLoading"
                  >
                    <option value="null">No expiry</option>
                    <option value="1">1 hour</option>
                    <option value="24">24 hours</option>
                    <option value="168">7 days</option>
                  </select>
                </div>
              </div>

              <!-- General Error Message from API -->
              <div v-if="error" class="api-error-card">
                <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <span>{{ error }}</span>
              </div>

              <button type="submit" class="submit-btn" :disabled="isLoading">
                <span v-if="isLoading" class="loader"></span>
                <span v-else>Shorten URL &rarr;</span>
              </button>
            </form>
          </div>
        </div>
      </section>

      <!-- RESULTS CARD -->
      <section v-if="result" class="result-section">
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
            <button @click="copyToClipboard(result.short_url)" class="action-btn">
              {{ copySuccess ? 'Copied!' : 'Copy' }}
            </button>
            <button @click="toggleQr(result.short_code)" class="action-btn" :class="{ 'btn-active': activeQrCode === result.short_code }">
              QR Code
            </button>
            <button @click="toggleStats(result.short_code)" class="action-btn" :class="{ 'btn-active': activeStats && activeStats.short_code === result.short_code }">
              View stats
            </button>
          </div>
        </div>

        <!-- Inline QR code viewer under result card -->
        <div v-if="activeQrCode === result.short_code" class="inline-qr-card">
          <div class="qr-content">
            <img :src="getQrUrl(result.short_code)" alt="QR Code" class="qr-image" />
            <div class="qr-details">
              <h4>Scan to visit</h4>
              <p>Scan this code to immediately open the shortened URL.</p>
              <a :href="getQrUrl(result.short_code)" download="qrcode.png" target="_blank" class="qr-download-link">
                Download PNG
              </a>
            </div>
          </div>
        </div>

        <!-- Inline Stats viewer under result card -->
        <div v-if="activeStats && activeStats.short_code === result.short_code" class="inline-stats-card">
          <div class="stats-header">
            <h4>Link Performance</h4>
          </div>
          <div class="stats-grid">
            <div class="stats-item">
              <span class="stats-label">Total Clicks</span>
              <span class="stats-val">{{ activeStats.click_count }}</span>
            </div>
            <div class="stats-item">
              <span class="stats-label">Created At</span>
              <span class="stats-val">{{ new Date(activeStats.created_at).toLocaleString() }}</span>
            </div>
            <div class="stats-item">
              <span class="stats-label">Expires At</span>
              <span class="stats-val">{{ activeStats.expires_at ? new Date(activeStats.expires_at).toLocaleString() : 'No expiry' }}</span>
            </div>
            <div class="stats-item">
              <span class="stats-label">Status</span>
              <span class="status-badge" :class="activeStats.is_expired ? 'badge-expired' : 'badge-active'">
                {{ activeStats.is_expired ? 'Expired' : 'Active' }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- RECENT LINKS SECTION -->
      <section class="recent-section">
        <div class="recent-header">
          <h2 class="section-title">Recent Links</h2>
          <a href="#" class="view-all-link" @click.prevent="fetchRecentLinks">Refresh table &rarr;</a>
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
              <template v-if="isLoadingRecent">
                <tr v-for="i in 3" :key="'skeleton-'+i">
                  <td><div class="skeleton skeleton-text" style="width: 140px; height: 16px;"></div></td>
                  <td><div class="skeleton skeleton-text" style="width: 250px; height: 16px;"></div></td>
                  <td><div class="skeleton skeleton-text" style="width: 40px; height: 16px; margin: 0 auto;"></div></td>
                  <td><div class="skeleton skeleton-text" style="width: 100px; height: 16px;"></div></td>
                  <td><div class="skeleton skeleton-text" style="width: 80px; height: 16px; margin: 0 auto;"></div></td>
                </tr>
              </template>

              <!-- Empty State -->
              <tr v-else-if="recentLinks.length === 0">
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
                <template v-for="link in recentLinks" :key="link.short_code">
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
                        <button class="icon-btn" title="View Stats" @click="toggleStats(link.short_code)" :class="{ 'icon-active': activeStats && activeStats.short_code === link.short_code }">
                          <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                            <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/>
                          </svg>
                        </button>
                        <button class="icon-btn" title="QR Code" @click="toggleQr(link.short_code)" :class="{ 'icon-active': activeQrCode === link.short_code }">
                          <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                            <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm2 2V5h1v1H5zm3 4a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 01-1 1H9a1 1 0 01-1-1v-3zm2 2v-1h1v1h-1zM3 12a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 01-1 1H4a1 1 0 01-1-1v-3zm2 2v-1h1v1H5zm10-7h-2V5h2v2zm0 5h-2v2h2v-2z" clip-rule="evenodd"/>
                            <path d="M13 10h2v1h-2v-1zM11 15h1v1h-1v-1zM13 14h1v1h-1v-1zM10 14h1v1h-1v-1zM12 11h1v1h-1v-1zM14 13h1v1h-1v-1zM15 16h1v1h-1v-1zM16 14h1v1h-1v-1zM16 11h1v1h-1v-1zM15 12h1v1h-1v-1zM12 13h1v1h-1v-1z"/>
                          </svg>
                        </button>
                        <button class="icon-btn btn-dot" title="Options" @click="copyToClipboard(link.short_url)">
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
                        <div class="qr-content">
                          <img :src="getQrUrl(link.short_code)" alt="QR Code" class="qr-image" />
                          <div class="qr-details">
                            <h4>QR Code for {{ link.short_code }}</h4>
                            <p>Scan this code to immediately open the shortened URL: <a :href="link.short_url" target="_blank">{{ link.short_url }}</a></p>
                            <a :href="getQrUrl(link.short_code)" download="qrcode.png" target="_blank" class="qr-download-link">
                              Download PNG
                            </a>
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>

                  <!-- Expandable Row for Stats in Table -->
                  <tr v-if="activeStats && activeStats.short_code === link.short_code" :key="'stats-'+link.short_code">
                    <td colspan="5" class="table-expand-cell">
                      <div class="expand-wrapper">
                        <div class="inline-stats-card" style="margin-top: 0; box-shadow: none; border: none; padding: 12px 16px;">
                          <div class="stats-grid">
                            <div class="stats-item">
                              <span class="stats-label">Total Clicks</span>
                              <span class="stats-val">{{ activeStats.click_count }}</span>
                            </div>
                            <div class="stats-item">
                              <span class="stats-label">Created At</span>
                              <span class="stats-val">{{ new Date(activeStats.created_at).toLocaleString() }}</span>
                            </div>
                            <div class="stats-item">
                              <span class="stats-label">Expires At</span>
                              <span class="stats-val">{{ activeStats.expires_at ? new Date(activeStats.expires_at).toLocaleString() : 'No expiry' }}</span>
                            </div>
                            <div class="stats-item">
                              <span class="stats-label">Status</span>
                              <span class="status-badge" :class="activeStats.is_expired ? 'badge-expired' : 'badge-active'">
                                {{ activeStats.is_expired ? 'Expired' : 'Active' }}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>
                </template>
              </template>
            </tbody>
          </table>
        </div>
      </section>

      <!-- FEATURES SECTION -->
      <section id="features" class="features-section">
        <div class="features-header">
          <span class="features-eyebrow">FEATURES</span>
          <h2 class="features-heading">Everything you need</h2>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <Zap :size="20" class="feature-icon" />
            </div>
            <h3 class="feature-title">Instant Shortening</h3>
            <p class="feature-desc">Generate short links in milliseconds with our optimized backend</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <BarChart2 :size="20" class="feature-icon" />
            </div>
            <h3 class="feature-title">Click Analytics</h3>
            <p class="feature-desc">Track every click with real-time statistics and performance data</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <QrCode :size="20" class="feature-icon" />
            </div>
            <h3 class="feature-title">QR Code</h3>
            <p class="feature-desc">Auto-generate QR code for every short link, ready to download</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <Timer :size="20" class="feature-icon" />
            </div>
            <h3 class="feature-title">Link Expiry</h3>
            <p class="feature-desc">Set links to expire automatically after hours or days</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <ShieldCheck :size="20" class="feature-icon" />
            </div>
            <h3 class="feature-title">Rate Limited</h3>
            <p class="feature-desc">Protected against spam and abuse with built-in rate limiting</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <Link :size="20" class="feature-icon" />
            </div>
            <h3 class="feature-title">Custom Alias</h3>
            <p class="feature-desc">Create memorable short links with your own custom names</p>
          </div>
        </div>
      </section>
    </main>

    <!-- ABOUT SECTION -->
    <section id="about" class="about-section">
      <div class="about-container">
        <!-- Left Content -->
        <div class="about-left">
          <span class="about-badge">Open Source</span>
          <h2 class="about-heading">Built for developers,<br>loved by everyone</h2>
          <p class="about-desc">
            Lnk.sh is a fast, simple URL shortener with built-in analytics and QR code generation. Built with FastAPI and Vue 3, designed to be clean and easy to use.
          </p>
          <a
            href="https://github.com/khanifnaufal/url-shortener-api"
            target="_blank"
            rel="noopener noreferrer"
            class="about-github-btn"
          >
            <Github :size="16" />
            <span>View on GitHub</span>
            <ArrowRight :size="14" class="arrow-icon" />
          </a>
        </div>

        <!-- Right Stats Cards -->
        <div class="about-right">
          <div class="stats-grid-about">
            <!-- Card 1 -->
            <div class="about-card">
              <div class="about-card-icon-wrapper">
                <Server :size="24" />
              </div>
              <span class="about-card-number">6</span>
              <span class="about-card-label">API Endpoints</span>
            </div>

            <!-- Card 2 -->
            <div class="about-card">
              <div class="about-card-icon-wrapper">
                <Gauge :size="24" />
              </div>
              <span class="about-card-number">&lt; 100ms</span>
              <span class="about-card-label">Response Time</span>
            </div>

            <!-- Card 3 -->
            <div class="about-card">
              <div class="about-card-icon-wrapper">
                <Layers :size="24" />
              </div>
              <span class="about-card-number">QR + Stats</span>
              <span class="about-card-label">Built-in Features</span>
            </div>

            <!-- Card 4 -->
            <div class="about-card">
              <div class="about-card-icon-wrapper">
                <Heart :size="24" />
              </div>
              <span class="about-card-number">Free</span>
              <span class="about-card-label">Open Source</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer-container">
        <span class="footer-text">&copy; {{ new Date().getFullYear() }} Shrinkr. All rights reserved.</span>
        <div class="footer-links">
          <a :href="apiDocsUrl" target="_blank" rel="noopener noreferrer" class="footer-link">
            API Docs
          </a>
          <a href="https://github.com/khanifnaufal/url-shortener-api" target="_blank" rel="noopener noreferrer" class="footer-link">
            GitHub
          </a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
html {
  scroll-behavior: smooth;
}
</style>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

/* NAVBAR */
.navbar {
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
}

.indigo-dot {
  color: var(--primary-color);
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: color 0.2s;
}

.nav-link:hover {
  color: var(--text-primary);
}

.api-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.api-link:hover {
  color: var(--primary-color) !important;
}

.api-link .nav-icon-right {
  transition: transform 0.2s ease;
}

.api-link:hover .nav-icon-right {
  transform: translate(2px, -2px);
}

.nav-link-disabled {
  pointer-events: none;
  opacity: 0.5;
}

.github-btn {
  background-color: #111827;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s, transform 0.2s, box-shadow 0.2s;
}

.github-btn:hover {
  background-color: #1f2937;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(17, 24, 39, 0.15);
}

.github-btn svg {
  transition: transform 0.2s ease;
}

.github-btn:hover svg {
  transform: scale(1.1);
}

.github-btn:active {
  transform: translateY(0) scale(0.98);
}

/* MAIN CONTENT */
.main-content {
  flex-grow: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 64px 24px;
  display: flex;
  flex-direction: column;
  gap: 48px;
}

@media (max-width: 768px) {
  .main-content {
    padding: 32px 16px;
    gap: 32px;
  }
}

/* HERO SECTION */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 48px;
}

@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}

.hero-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}

.hero-heading {
  font-size: 48px;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -1.5px;
  color: var(--text-primary);
  white-space: pre-line;
}

@media (max-width: 1024px) {
  .hero-heading {
    font-size: 40px;
  }
}

@media (max-width: 480px) {
  .hero-heading {
    font-size: 32px;
  }
}

.hero-subtext {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.6;
  white-space: pre-line;
}

/* FORM CARD */
.form-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 32px;
  box-shadow: var(--shadow-card);
  text-align: left;
}

@media (max-width: 480px) {
  .form-card {
    padding: 24px 16px;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 480px) {
  .form-row {
    flex-direction: column;
    gap: 20px;
  }
}

.col-half {
  flex: 1;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input,
.form-select {
  height: 48px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  padding: 0 16px;
  font-size: 15px;
  background-color: #FFFFFF;
  transition: border-color 0.2s, box-shadow 0.2s;
  width: 100%;
  outline: none;
}

.form-input::placeholder {
  color: #9CA3AF;
}

.form-input:focus,
.form-select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12);
}

.input-error {
  border-color: #EF4444;
}

.input-error:focus {
  border-color: #EF4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.12);
}

.error-text {
  font-size: 13px;
  color: #EF4444;
  margin-top: 2px;
}

.api-error-card {
  background-color: #FEF2F2;
  border: 1px solid #FEE2E2;
  border-radius: 8px;
  padding: 12px 16px;
  color: #B91C1C;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.submit-btn {
  background-color: #111827;
  color: #FFFFFF;
  width: 100%;
  height: 50px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s, transform 0.1s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #1f2937;
}

.submit-btn:active:not(:disabled) {
  transform: scale(0.99);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* RESULTS CARD */
.result-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

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

/* INLINE QR CARD */
.inline-qr-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-card);
}

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
}

.qr-details p {
  font-size: 14px;
  color: var(--text-secondary);
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

/* INLINE STATS CARD */
.inline-stats-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-card);
  text-align: left;
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

/* RECENT LINKS SECTION */
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
/* Spinner Loader */
.loader {
  width: 20px;
  height: 20px;
  border: 2px solid #FFF;
  border-bottom-color: transparent;
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  animation: rotation 1s infinite linear;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* FEATURES SECTION */
.features-section {
  padding: 80px 0;
  text-align: left;
}

.features-header {
  margin-bottom: 48px;
}

.features-eyebrow {
  font-size: 12px;
  font-weight: 700;
  color: #6366F1;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  display: block;
  margin-bottom: 8px;
}

.features-heading {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin-top: 0;
  margin-bottom: 48px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  background-color: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  transition: transform 0.2s, box-shadow 0.2s;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.feature-icon-wrapper {
  background-color: rgba(99, 102, 241, 0.1);
  color: #6366F1;
  border-radius: 8px;
  padding: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.feature-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-top: 16px;
  margin-bottom: 0;
}

.feature-desc {
  font-size: 14px;
  color: #6B7280;
  margin-top: 6px;
  margin-bottom: 0;
  line-height: 1.6;
}

/* Responsive grid for features */
@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
  .features-section {
    padding: 60px 0;
  }
  .features-heading {
    font-size: 28px;
    margin-bottom: 32px;
  }
}

/* ABOUT SECTION */
.about-section {
  background-color: #F9FAFB;
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
  width: 100%;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 64px;
}

.about-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.about-badge {
  display: inline-flex;
  align-items: center;
  border: 1px solid rgba(99, 102, 241, 0.3);
  color: var(--primary-color);
  background-color: rgba(99, 102, 241, 0.05);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.about-heading {
  font-size: 38px;
  font-weight: 800;
  color: var(--text-primary);
  margin-top: 16px;
  line-height: 1.25;
  letter-spacing: -1px;
  white-space: pre-line;
}

.about-desc {
  color: #6B7280;
  line-height: 1.7;
  margin-top: 16px;
  font-size: 16px;
}

.about-github-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: 1px solid #111827;
  background-color: transparent;
  color: #111827;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  margin-top: 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  width: fit-content;
}

.about-github-btn:hover {
  background-color: #111827;
  color: #FFFFFF;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(17, 24, 39, 0.15);
}

.about-github-btn:active {
  transform: translateY(0);
}

.about-github-btn svg {
  transition: transform 0.2s ease;
}

.about-github-btn:hover .arrow-icon {
  transform: translateX(3px);
}

.stats-grid-about {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.about-card {
  background-color: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 24px 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.about-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.05), 0 8px 8px -6px rgba(0, 0, 0, 0.05);
  border-color: rgba(99, 102, 241, 0.2);
}

.about-card-icon-wrapper {
  background-color: rgba(99, 102, 241, 0.08);
  color: #6366F1;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  transition: transform 0.3s ease;
}

.about-card:hover .about-card-icon-wrapper {
  transform: scale(1.1) rotate(4deg);
}

.about-card-number {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
  letter-spacing: -0.5px;
}

.about-card-number-large {
  font-size: 24px;
}

.about-card-label {
  font-size: 13px;
  color: #6B7280;
  font-weight: 500;
}

/* FOOTER */
.footer {
  background-color: #FFFFFF;
  border-top: 1px solid var(--border-color);
  padding: 32px 0;
  width: 100%;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text {
  font-size: 14px;
  color: #6B7280;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-link {
  font-size: 14px;
  color: #6B7280;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--primary-color);
}

@media (max-width: 1024px) {
  .about-container {
    gap: 40px;
  }
  .about-heading {
    font-size: 32px;
  }
}

@media (max-width: 768px) {
  .about-container {
    grid-template-columns: 1fr;
    gap: 48px;
    padding: 60px 24px;
  }
  .about-left {
    align-items: center;
    text-align: center;
  }
}

@media (max-width: 640px) {
  .footer-container {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .stats-grid-about {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .about-heading {
    font-size: 28px;
  }
}
</style>
