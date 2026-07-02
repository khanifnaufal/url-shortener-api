import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { shortenUrl, getUrls, getStats, getQrUrl } from '../api/shortener.js'

export function useUrlShortener() {
  const router = useRouter()

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
  async function handleShorten(payload) {
    error.value = null
    inlineValidationError.value = ''
    
    let urlToShorten = longUrl.value
    let alias = customAlias.value
    let expIn = expiresIn.value

    if (payload) {
      urlToShorten = payload.longUrl
      alias = payload.customAlias
      expIn = payload.expiresIn
    }

    // Validate longUrl is not empty
    if (!urlToShorten || !urlToShorten.trim()) {
      inlineValidationError.value = 'Please enter a long URL.'
      return
    }

    // Basic URL format validation
    try {
      new URL(urlToShorten)
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
    if (expIn !== 'null') {
      hours = parseInt(expIn, 10)
    }

    try {
      const data = await shortenUrl(
        urlToShorten.trim(),
        alias ? alias.trim() : null,
        hours
      )
      result.value = data
      
      // Clear form inputs except expiresIn
      longUrl.value = ''
      customAlias.value = ''
      
      // Refresh table
      await fetchRecentLinks()
    } catch (err) {
      if (!err.response) {
        // Network error (no response received)
        error.value = 'Unable to connect to server. Please check your connection.'
      } else if (err.response.status === 429) {
        // Rate limit exceeded
        error.value = 'Too many requests. Please wait a moment before trying again.'
      } else if (err.response.status === 400) {
        const detail = err.response.data?.detail || ''
        if (typeof detail === 'string' && detail.toLowerCase().includes('alias')) {
          error.value = 'This custom alias is already taken. Try another one.'
        } else if (typeof detail === 'string' && (detail.toLowerCase().includes('url') || detail.toLowerCase().includes('valid'))) {
          error.value = 'Please enter a valid URL starting with http:// or https://'
        } else {
          // Fallback for other 400 errors — do not expose technical message
          error.value = 'Invalid request. Please check your input and try again.'
        }
      } else if (err.response.data?.detail) {
        // Any other structured API error — use a generic user-friendly fallback
        error.value = 'Something went wrong. Please try again.'
      } else {
        error.value = 'An unexpected error occurred. Please try again.'
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
  function toggleStats(shortCode) {
    router.push(`/stats/${shortCode}`)
  }

  return {
    longUrl,
    customAlias,
    expiresIn,
    result,
    recentLinks,
    isLoading,
    isLoadingRecent,
    error,
    inlineValidationError,
    activeQrCode,
    activeStats,
    isLoadingStats,
    copySuccess,
    timeAgo,
    fetchRecentLinks,
    handleShorten,
    copyToClipboard,
    toggleQr,
    toggleStats
  }
}
