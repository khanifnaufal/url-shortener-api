<script setup>
defineProps({
  apiDocsUrl: {
    type: String,
    required: true
  }
})
</script>

<template>
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
</template>

<style scoped>
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

@media (max-width: 640px) {
  .footer-container {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>
