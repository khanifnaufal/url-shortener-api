<script setup>
import { onMounted, provide } from 'vue'
import { useUrlShortener } from '../composables/useUrlShortener'
import { getQrUrl } from '../api/shortener.js'

// Import components
import NavBar from '../components/NavBar.vue'
import HeroSection from '../components/HeroSection.vue'
import UrlForm from '../components/UrlForm.vue'
import ResultCard from '../components/ResultCard.vue'
import QrCodeCard from '../components/QrCodeCard.vue'
import StatsCard from '../components/StatsCard.vue'
import RecentLinksTable from '../components/RecentLinksTable.vue'
import FeaturesSection from '../components/FeaturesSection.vue'
import AboutSection from '../components/AboutSection.vue'
import AppFooter from '../components/AppFooter.vue'

const {
  result,
  recentLinks,
  isLoading,
  isLoadingRecent,
  error,
  activeQrCode,
  activeStats,
  copySuccess,
  timeAgo,
  fetchRecentLinks,
  handleShorten,
  copyToClipboard,
  toggleQr,
  toggleStats
} = useUrlShortener()

// Provide getQrUrl to descendant components like QrCodeCard
provide('getQrUrl', getQrUrl)

const apiDocsUrl = import.meta.env.VITE_API_BASE_URL + '/docs'

onMounted(() => {
  fetchRecentLinks()
})

function scrollToSection(id) {
  document.getElementById(id)?.scrollIntoView({ 
    behavior: 'smooth' 
  })
}
</script>

<template>
  <div class="home-container">
    <NavBar 
      :api-docs-url="apiDocsUrl"
      @scroll-to-features="scrollToSection('features')"
      @scroll-to-about="scrollToSection('about')"
    />
    
    <main class="main-content">
      <!-- HERO & FORM SECTION -->
      <section class="hero-section">
        <HeroSection />
        <UrlForm 
          :is-loading="isLoading" 
          :error="error"
          :result="result"
          @submit="handleShorten"
        />
      </section>

      <!-- RESULTS CARD -->
      <section v-if="result" class="result-section">
        <ResultCard 
          :result="result"
          :copy-success="copySuccess"
          :active-qr-code="activeQrCode"
          :active-stats="activeStats"
          @copy="copyToClipboard(result.short_url)"
          @toggle-qr="toggleQr"
          @toggle-stats="toggleStats"
        />

        <!-- Inline QR code viewer under result card -->
        <div v-if="activeQrCode === result.short_code" class="inline-qr-card">
          <QrCodeCard :short-code="result.short_code" :short-url="result.short_url" />
        </div>

        <!-- Inline Stats viewer under result card -->
        <StatsCard 
          v-if="activeStats && activeStats.short_code === result.short_code" 
          :stats="activeStats" 
        />
      </section>

      <!-- RECENT LINKS SECTION -->
      <RecentLinksTable 
        :links="recentLinks"
        :is-loading="isLoadingRecent"
        :active-qr-code="activeQrCode"
        :active-stats="activeStats"
        :time-ago="timeAgo"
        @toggle-qr="toggleQr"
        @toggle-stats="toggleStats"
        @copy="copyToClipboard"
        @refresh="fetchRecentLinks"
      />

      <!-- FEATURES SECTION -->
      <FeaturesSection />
    </main>

    <!-- ABOUT SECTION -->
    <AboutSection />

    <!-- FOOTER -->
    <AppFooter :api-docs-url="apiDocsUrl" />
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

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

.result-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.inline-qr-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-card);
}
</style>
