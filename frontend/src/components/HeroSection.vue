<template>
  <div class="hero-left">
    <h1 class="hero-heading">Shorten links,<br>share anywhere.</h1>
    <p class="hero-subtext">Paste a long URL and get a short link instantly.<br>Fast. Simple. Reliable.</p>
  </div>
</template>

<style scoped>
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
</style>
