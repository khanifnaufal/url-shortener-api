<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  result: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit'])

const longUrl = ref('')
const customAlias = ref('')
const expiresIn = ref('null')
const inlineValidationError = ref('')

function handleSubmit() {
  inlineValidationError.value = ''
  
  if (!longUrl.value.trim()) {
    inlineValidationError.value = 'Please enter a long URL.'
    return
  }

  try {
    new URL(longUrl.value)
  } catch (_) {
    inlineValidationError.value = 'Please enter a valid URL (e.g. https://google.com).'
    return
  }

  emit('submit', {
    longUrl: longUrl.value.trim(),
    customAlias: customAlias.value.trim() || null,
    expiresIn: expiresIn.value
  })
}

// Reset inputs when a result is successfully created
watch(() => props.result, (newVal) => {
  if (newVal) {
    longUrl.value = ''
    customAlias.value = ''
  }
})
</script>

<template>
  <div class="hero-right">
    <div class="form-card">
      <form @submit.prevent="handleSubmit">
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
</template>

<style scoped>
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
    padding: 16px;
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
</style>
