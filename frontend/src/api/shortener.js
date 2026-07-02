import axios from 'axios'

/**
 * Axios instance yang dikonfigurasi untuk berkomunikasi dengan backend URL Shortener API.
 * - baseURL diambil dari environment variable VITE_API_BASE_URL
 * - Header X-API-Key dikirim otomatis di setiap request menggunakan interceptor
 */
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor — tambahkan X-API-Key otomatis ke setiap request
apiClient.interceptors.request.use((config) => {
  const apiKey = import.meta.env.VITE_API_KEY
  if (apiKey) {
    config.headers['X-API-Key'] = apiKey
  }
  return config
})

/**
 * Memperpendek URL panjang menjadi short URL.
 *
 * @param {string} longUrl - URL panjang yang akan diperpendek (wajib)
 * @param {string|null} customAlias - Alias kustom opsional (misal: "google")
 * @param {number|null} expiresInHours - Masa berlaku dalam jam, null = tidak ada expiry
 * @returns {Promise<Object>} Response: { short_code, short_url, long_url, created_at, expires_at }
 */
export async function shortenUrl(longUrl, customAlias = null, expiresInHours = null) {
  const payload = { long_url: longUrl }

  if (customAlias) {
    payload.custom_alias = customAlias
  }
  if (expiresInHours !== null && expiresInHours !== undefined) {
    payload.expires_in_hours = expiresInHours
  }

  const response = await apiClient.post('/shorten', payload)
  return response.data
}

/**
 * Mendapatkan statistik untuk sebuah short code.
 *
 * @param {string} shortCode - Short code yang ingin dicek (misal: "google")
 * @returns {Promise<Object>} Response: { short_code, long_url, click_count, created_at, expires_at, is_expired, qr_url }
 */
export async function getStats(shortCode) {
  const response = await apiClient.get(`/stats/${shortCode}`)
  return response.data
}

/**
 * Mendapatkan URL ke endpoint QR code untuk ditampilkan sebagai <img src="">.
 * Fungsi ini TIDAK melakukan fetch — hanya mengembalikan URL string.
 *
 * Contoh penggunaan di template Vue:
 *   <img :src="getQrUrl('google')" alt="QR Code" />
 *
 * @param {string} shortCode - Short code yang ingin digenerate QR-nya
 * @returns {string} URL lengkap ke endpoint /qr/{shortCode}
 */
export function getQrUrl(shortCode) {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  return `${baseURL}/qr/${shortCode}`
}

export default apiClient
