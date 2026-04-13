<template>
  <div class="da-weather-card">
    <div class="da-weather-date">{{ weather.date }}</div>
    <div class="da-weather-split">
      <div class="da-weather-part">
        <span class="da-weather-icon">☀️</span>
        <div class="da-weather-details">
          <span class="da-w-label">Day</span>
          <span class="da-w-value">{{ weather.day_weather }} {{ weather.day_temp }}°C</span>
        </div>
      </div>
      <div class="da-weather-part">
        <span class="da-weather-icon">🌙</span>
        <div class="da-weather-details">
          <span class="da-w-label">Night</span>
          <span class="da-w-value">{{ weather.night_weather }} {{ weather.night_temp }}°C</span>
        </div>
      </div>
    </div>
    <div class="da-weather-wind">
      💨 {{ weather.wind_direction }} {{ weather.wind_power }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import type { WeatherInfo } from '@/types'

defineProps<{
  weather: WeatherInfo
}>()
</script>

<style scoped>
.da-weather-card {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}
.da-weather-card:hover {
  transform: translateY(-2px);
}
.da-weather-date {
  font-weight: 700;
  color: var(--da-text-main);
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  padding-bottom: 8px;
}
.da-weather-split {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}
.da-weather-part {
  display: flex;
  align-items: center;
  gap: 12px;
}
.da-weather-icon {
  font-size: 24px;
}
.da-weather-details {
  display: flex;
  flex-direction: column;
}
.da-w-label {
  font-size: 12px;
  color: var(--da-text-light);
}
.da-w-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--da-text-main);
}
.da-weather-wind {
  font-size: 13px;
  color: var(--da-text-light);
  background: rgba(255,255,255,0.5);
  padding: 4px 8px;
  border-radius: 8px;
  display: inline-block;
}
</style>
