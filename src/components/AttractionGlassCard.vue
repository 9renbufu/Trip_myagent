<template>
  <div class="da-masonry-card">
    <div class="da-card-image-wrapper">
      <img v-if="photoUrl" :src="photoUrl" :alt="attraction.name" class="da-card-image" @error="handleImageError" />
      <div v-else class="da-card-image-placeholder">加载中...</div>
      <div v-if="attraction.ticket_price" class="da-attr-price">¥{{ attraction.ticket_price }}</div>
    </div>
    
    <div class="da-card-content">
      <div class="da-card-header">
        <h4 class="da-attr-name">{{ attraction.name }}</h4>
      </div>
      
      <div class="da-attr-body">
        <p class="da-attr-desc">{{ attraction.description }}</p>
        
        <div class="da-attr-meta">
          <span class="da-meta-item">📍 {{ attraction.address }}</span>
          <span class="da-meta-item">⏱️ {{ attraction.visit_duration }} mins</span>
          <span v-if="attraction.rating" class="da-meta-item">⭐ {{ attraction.rating }}</span>
        </div>
      </div>

      <!-- Edit Mode Controls -->
      <div v-if="editMode" class="da-edit-controls">
        <a-button size="small" @click="$emit('moveUp')" :disabled="isFirst">↑</a-button>
        <a-button size="small" @click="$emit('moveDown')" :disabled="isLast">↓</a-button>
        <a-button size="small" danger @click="$emit('delete')">🗑️</a-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps, defineEmits } from 'vue'
import type { Attraction } from '@/types'

const props = defineProps<{
  attraction: Attraction
  editMode: boolean
  isFirst: boolean
  isLast: boolean
}>()

defineEmits(['moveUp', 'moveDown', 'delete'])

const photoUrl = ref<string>('')

onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:8000/api/poi/photo?name=${encodeURIComponent(props.attraction.name)}`)
    const data = await res.json()
    if (data.success && data.data.photo_url) {
      photoUrl.value = data.data.photo_url
    } else {
      photoUrl.value = getFallbackImage(props.attraction.name)
    }
  } catch (error) {
    console.error(`Failed to fetch photo for ${props.attraction.name}:`, error)
    photoUrl.value = getFallbackImage(props.attraction.name)
  }
})

const getFallbackImage = (name: string): string => {
  const colors = [
    { start: '#667eea', end: '#764ba2' },
    { start: '#f093fb', end: '#f5576c' },
    { start: '#4facfe', end: '#00f2fe' },
    { start: '#43e97b', end: '#38f9d7' },
    { start: '#fa709a', end: '#fee140' }
  ]
  const colorIndex = Math.floor(Math.random() * colors.length)
  const { start, end } = colors[colorIndex]

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">
    <defs>
      <linearGradient id="grad${colorIndex}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:${start};stop-opacity:1" />
        <stop offset="100%" style="stop-color:${end};stop-opacity:1" />
      </linearGradient>
    </defs>
    <rect width="400" height="300" fill="url(#grad${colorIndex})"/>
    <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="24" font-weight="bold" fill="white">${name}</text>
  </svg>`

  return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = getFallbackImage(props.attraction.name)
}
</script>

<style scoped>
.da-masonry-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  margin-bottom: 20px;
  break-inside: avoid;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.da-masonry-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
}

.da-card-image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f0f0f0;
}

.da-card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.da-card-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 14px;
}

.da-masonry-card:hover .da-card-image {
  transform: scale(1.05);
}

.da-attr-price {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(239, 68, 68, 0.9);
  backdrop-filter: blur(4px);
  color: white;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.da-card-content {
  padding: 20px;
}

.da-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.da-attr-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--da-text-main);
  margin: 0;
  line-height: 1.3;
}

.da-attr-desc {
  color: var(--da-text-light);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.da-attr-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(255, 255, 255, 0.5);
  padding: 12px;
  border-radius: 12px;
}

.da-meta-item {
  font-size: 13px;
  color: #475569;
  display: flex;
  align-items: center;
  gap: 6px;
}

.da-edit-controls {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px dashed rgba(0,0,0,0.1);
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
</style>
