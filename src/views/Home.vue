<template>
  <div class="da-home-wrapper">
    <div class="da-content-split">
      <!-- Left side: Form -->
      <div class="da-form-side">
        <div class="da-intro-text">
          <h1 class="da-hero-title">Plan Your Next Adventure</h1>
          <p class="da-hero-subtitle">Let AI craft the perfect itinerary tailored to your style.</p>
        </div>

        <div class="da-glass-panel">
          <a-form
            :model="tripRequest"
            layout="vertical"
            @finish="onFormSubmit"
            class="da-trip-form"
          >
            <!-- Destination & Dates -->
            <div class="da-form-group">
              <h3 class="da-group-title"><span class="da-emoji">📍</span> Where & When</h3>
              
              <a-form-item name="city" :rules="[{ required: true, message: 'Destination is required' }]">
                <template #label><span class="da-label">Destination City</span></template>
                <a-input
                  v-model:value="tripRequest.city"
                  placeholder="e.g. Tokyo, Paris"
                  size="large"
                  class="da-glass-input"
                />
              </a-form-item>

              <div class="da-date-row">
                <a-form-item name="start_date" :rules="[{ required: true, message: 'Start date needed' }]" class="da-flex-1">
                  <template #label><span class="da-label">Start Date</span></template>
                  <a-date-picker
                    v-model:value="tripRequest.start_date"
                    style="width: 100%"
                    size="large"
                    class="da-glass-input"
                  />
                </a-form-item>
                
                <a-form-item name="end_date" :rules="[{ required: true, message: 'End date needed' }]" class="da-flex-1">
                  <template #label><span class="da-label">End Date</span></template>
                  <a-date-picker
                    v-model:value="tripRequest.end_date"
                    style="width: 100%"
                    size="large"
                    class="da-glass-input"
                  />
                </a-form-item>
              </div>
              
              <div class="da-days-indicator" v-if="tripRequest.travel_days > 0">
                Duration: <strong>{{ tripRequest.travel_days }}</strong> days
              </div>
            </div>

            <!-- Preferences -->
            <div class="da-form-group">
              <h3 class="da-group-title"><span class="da-emoji">✨</span> Your Style</h3>
              
              <div class="da-select-row">
                <a-form-item name="transportation" class="da-flex-1">
                  <template #label><span class="da-label">Transport</span></template>
                  <a-select v-model:value="tripRequest.transportation" size="large" class="da-glass-select">
                    <a-select-option value="公共交通">🚇 Public Transit</a-select-option>
                    <a-select-option value="自驾">🚗 Driving</a-select-option>
                    <a-select-option value="步行">🚶 Walking</a-select-option>
                    <a-select-option value="混合">🔀 Mixed</a-select-option>
                  </a-select>
                </a-form-item>
                
                <a-form-item name="accommodation" class="da-flex-1">
                  <template #label><span class="da-label">Stay</span></template>
                  <a-select v-model:value="tripRequest.accommodation" size="large" class="da-glass-select">
                    <a-select-option value="经济型酒店">💰 Budget</a-select-option>
                    <a-select-option value="舒适型酒店">🏨 Comfort</a-select-option>
                    <a-select-option value="豪华酒店">⭐ Luxury</a-select-option>
                    <a-select-option value="民宿">🏡 Airbnb/B&B</a-select-option>
                  </a-select>
                </a-form-item>
              </div>

              <a-form-item name="preferences">
                <template #label><span class="da-label">Interests</span></template>
                <a-checkbox-group v-model:value="tripRequest.preferences" class="da-glass-checkbox-group">
                  <a-checkbox value="历史文化" class="da-glass-checkbox">🏛️ Culture</a-checkbox>
                  <a-checkbox value="自然风光" class="da-glass-checkbox">🏞️ Nature</a-checkbox>
                  <a-checkbox value="美食" class="da-glass-checkbox">🍜 Food</a-checkbox>
                  <a-checkbox value="购物" class="da-glass-checkbox">🛍️ Shopping</a-checkbox>
                  <a-checkbox value="艺术" class="da-glass-checkbox">🎨 Art</a-checkbox>
                  <a-checkbox value="休闲" class="da-glass-checkbox">☕ Relax</a-checkbox>
                </a-checkbox-group>
              </a-form-item>
            </div>

            <!-- Extra -->
            <div class="da-form-group">
              <h3 class="da-group-title"><span class="da-emoji">💬</span> Extra Notes</h3>
              <a-form-item name="free_text_input">
                <a-textarea
                  v-model:value="tripRequest.free_text_input"
                  placeholder="Any special requests? e.g., vegan, accessible..."
                  :rows="3"
                  class="da-glass-input"
                />
              </a-form-item>
            </div>

            <!-- Submit & Loading -->
            <div class="da-action-area">
              <button v-if="!isProcessing" type="submit" class="da-submit-btn">
                Generate Itinerary ✈️
              </button>
              
              <div v-else class="da-loading-wrapper">
                <div class="da-custom-loader">
                  <div class="da-dot"></div>
                  <div class="da-dot"></div>
                  <div class="da-dot"></div>
                </div>
                <div class="da-loading-text">{{ currentStatusText }}</div>
              </div>
            </div>
          </a-form>
        </div>
      </div>

      <!-- Right side: Visuals -->
      <div class="da-visual-side">
        <div class="da-visual-card">
          <div class="da-visual-content">
            <h2>Discover the Unseen</h2>
            <p>Your personal AI travel concierge is ready.</p>
            <div class="da-visual-decor">
               <div class="da-glass-circle top-right"></div>
               <div class="da-glass-circle bottom-left"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { generateTripPlan } from '@/services/api'
import type { TripFormData } from '@/types'
import type { Dayjs } from 'dayjs'

const router = useRouter()
const isProcessing = ref(false)
const currentStatusText = ref('')

const tripRequest = reactive<Omit<TripFormData, 'start_date' | 'end_date'> & { start_date: Dayjs | null; end_date: Dayjs | null }>({
  city: '',
  start_date: null,
  end_date: null,
  travel_days: 1,
  transportation: '公共交通',
  accommodation: '舒适型酒店',
  preferences: [],
  free_text_input: ''
})

watch([() => tripRequest.start_date, () => tripRequest.end_date], ([start, end]) => {
  if (start && end) {
    const daysCount = end.diff(start, 'day') + 1
    if (daysCount > 0 && daysCount <= 30) {
      tripRequest.travel_days = daysCount
    } else if (daysCount > 30) {
      message.warning('Maximum travel duration is 30 days.')
      tripRequest.end_date = null
    } else {
      message.warning('End date cannot be earlier than start date.')
      tripRequest.end_date = null
    }
  }
})

const onFormSubmit = async () => {
  if (!tripRequest.start_date || !tripRequest.end_date) {
    message.error('Please select both start and end dates.')
    return
  }

  isProcessing.value = true
  currentStatusText.value = 'Initializing your journey...'

  let progress = 0
  const progressTimer = setInterval(() => {
    progress += 10
    if (progress <= 30) currentStatusText.value = '🔍 Finding the best spots...'
    else if (progress <= 60) currentStatusText.value = '🌤️ Checking local weather...'
    else if (progress <= 80) currentStatusText.value = '🏨 Curating stays & routes...'
    else currentStatusText.value = '✨ Finalizing itinerary...'
  }, 600)

  try {
    const payload: TripFormData = {
      city: tripRequest.city,
      start_date: tripRequest.start_date.format('YYYY-MM-DD'),
      end_date: tripRequest.end_date.format('YYYY-MM-DD'),
      travel_days: tripRequest.travel_days,
      transportation: tripRequest.transportation,
      accommodation: tripRequest.accommodation,
      preferences: tripRequest.preferences,
      free_text_input: tripRequest.free_text_input
    }

    const res = await generateTripPlan(payload)
    clearInterval(progressTimer)

    if (res.success && res.data) {
      currentStatusText.value = '✅ Done!'
      sessionStorage.setItem('tripPlan', JSON.stringify(res.data))
      message.success('Itinerary generated successfully!')
      setTimeout(() => {
        router.push('/result')
      }, 600)
    } else {
      message.error(res.message || 'Failed to generate itinerary.')
      isProcessing.value = false
    }
  } catch (err: any) {
    clearInterval(progressTimer)
    message.error(err.message || 'An error occurred. Please try again.')
    isProcessing.value = false
  }
}
</script>

<style scoped>
.da-home-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
}

.da-content-split {
  display: flex;
  width: 100%;
  gap: 40px;
  flex-wrap: wrap;
}

.da-form-side {
  flex: 1;
  min-width: 400px;
  max-width: 600px;
}

.da-visual-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 400px;
}

.da-intro-text {
  margin-bottom: 30px;
}

.da-hero-title {
  font-size: 42px;
  font-weight: 800;
  color: var(--da-text-main);
  line-height: 1.2;
  margin-bottom: 10px;
}

.da-hero-subtitle {
  font-size: 18px;
  color: var(--da-text-light);
}

.da-glass-panel {
  background: var(--da-bg-glass);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--da-border-glass);
  border-radius: 24px;
  padding: 30px;
  box-shadow: var(--da-shadow-glass);
}

.da-form-group {
  margin-bottom: 24px;
}

.da-group-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--da-text-main);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.da-label {
  font-weight: 500;
  color: var(--da-text-light);
}

.da-flex-1 {
  flex: 1;
}

.da-date-row, .da-select-row {
  display: flex;
  gap: 16px;
}

.da-days-indicator {
  font-size: 14px;
  color: var(--da-primary);
  background: rgba(59, 130, 246, 0.1);
  padding: 6px 12px;
  border-radius: 8px;
  display: inline-block;
  margin-bottom: 16px;
}

/* Custom Inputs styling */
:deep(.da-glass-input .ant-input),
:deep(.da-glass-input.ant-picker),
:deep(.da-glass-select .ant-select-selector) {
  background: rgba(255, 255, 255, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.5) !important;
  border-radius: 12px !important;
  backdrop-filter: blur(4px);
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
  transition: all 0.3s ease;
}

:deep(.da-glass-input .ant-input:focus),
:deep(.da-glass-input.ant-picker-focused),
:deep(.da-glass-select.ant-select-focused .ant-select-selector) {
  border-color: var(--da-primary) !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
  background: rgba(255, 255, 255, 0.7) !important;
}

/* Checkboxes */
.da-glass-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

:deep(.da-glass-checkbox.ant-checkbox-wrapper) {
  margin: 0 !important;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  backdrop-filter: blur(4px);
  transition: all 0.3s ease;
}

:deep(.da-glass-checkbox.ant-checkbox-wrapper-checked) {
  background: var(--da-primary);
  border-color: var(--da-primary);
  color: white;
}

:deep(.da-glass-checkbox.ant-checkbox-wrapper-checked .ant-checkbox-inner) {
  background-color: white;
  border-color: white;
}
:deep(.da-glass-checkbox.ant-checkbox-wrapper-checked .ant-checkbox-inner::after) {
  border-color: var(--da-primary);
}

/* Button */
.da-submit-btn {
  width: 100%;
  padding: 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--da-primary), #60a5fa);
  color: white;
  font-size: 18px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}

.da-submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 25px rgba(59, 130, 246, 0.4);
}

/* Custom Loader */
.da-loading-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: rgba(255,255,255,0.3);
  border-radius: 16px;
}

.da-custom-loader {
  display: flex;
  gap: 8px;
}

.da-dot {
  width: 12px;
  height: 12px;
  background-color: var(--da-primary);
  border-radius: 50%;
  animation: da-bounce 1.4s infinite ease-in-out both;
}

.da-dot:nth-child(1) { animation-delay: -0.32s; }
.da-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes da-bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.da-loading-text {
  color: var(--da-primary);
  font-weight: 500;
}

/* Visual Side */
.da-visual-card {
  position: relative;
  width: 100%;
  height: 600px;
  background: linear-gradient(135deg, rgba(255,255,255,0.4), rgba(255,255,255,0.1));
  backdrop-filter: blur(20px);
  border-radius: 32px;
  border: 1px solid var(--da-border-glass);
  box-shadow: var(--da-shadow-glass);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.da-visual-content {
  text-align: center;
  z-index: 2;
  color: var(--da-text-main);
  padding: 40px;
}

.da-visual-content h2 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #1e293b, var(--da-primary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.da-glass-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--da-primary), #8b5cf6);
  opacity: 0.6;
  filter: blur(40px);
  z-index: 1;
}

.top-right {
  width: 300px;
  height: 300px;
  top: -50px;
  right: -50px;
}

.bottom-left {
  width: 250px;
  height: 250px;
  bottom: -50px;
  left: -50px;
}
</style>
