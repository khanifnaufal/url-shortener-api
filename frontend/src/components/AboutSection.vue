<script setup>
import { Github, ArrowRight, Server, Gauge, Layers, Heart } from 'lucide-vue-next'
</script>

<template>
  <section id="about" class="about-section">
    <div class="about-container">
      <!-- Left Content -->
      <div class="about-left">
        <span class="about-badge">Open Source</span>
        <h2 class="about-heading">Built for developers,<br>loved by everyone</h2>
        <p class="about-desc">
         Shrinkr is an open-source URL shortener built 
with FastAPI and Vue 3. Shorten any link, track 
clicks in real-time, and generate QR codes — 
all in one clean, minimal interface.
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
</template>

<style scoped>
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
