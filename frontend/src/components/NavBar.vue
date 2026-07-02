<script setup>
import { Github, ExternalLink } from 'lucide-vue-next'

defineProps({
  apiDocsUrl: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['scrollToFeatures', 'scrollToAbout'])
</script>

<template>
  <nav class="navbar">
    <div class="nav-content">
      <div class="nav-left">
        <span class="logo">Shri<span class="indigo-dot">i</span>inkr<span class="indigo-dot">.</span></span>
      </div>
      <div class="nav-right">
        <div class="nav-links">
          <a href="#" class="nav-link" @click.prevent="emit('scrollToAbout')">About</a>
          <a href="#" class="nav-link" @click.prevent="emit('scrollToFeatures')">Features</a>
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
</template>

<style scoped>
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

@media (max-width: 480px) {
  .nav-links {
    display: none;
  }
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
</style>
