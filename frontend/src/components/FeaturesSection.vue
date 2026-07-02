<script setup>
import { Zap, BarChart2, QrCode, Timer, ShieldCheck, Link } from 'lucide-vue-next'
</script>

<template>
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
</template>

<style scoped>
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
</style>
