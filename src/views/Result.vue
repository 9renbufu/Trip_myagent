<template>
  <div class="da-result-wrapper">
    <!-- Header -->
    <div class="da-header-glass">
      <button class="da-btn da-btn-back" @click="goBack">← Back</button>
      
      <div class="da-header-actions">
        <button v-if="!isEditing" @click="toggleEdit" class="da-btn da-btn-edit">
          ✏️ Edit Plan
        </button>
        <button v-else @click="saveEdits" class="da-btn da-btn-primary">
          💾 Save Changes
        </button>
        <button v-if="isEditing" @click="cancelEdits" class="da-btn da-btn-cancel">
          ❌ Cancel
        </button>

        <!-- Export -->
        <a-dropdown v-if="!isEditing">
          <template #overlay>
            <a-menu>
              <a-menu-item key="image" @click="exportImage">📷 Export Image</a-menu-item>
              <a-menu-item key="pdf" @click="exportPdf">📄 Export PDF</a-menu-item>
            </a-menu>
          </template>
          <button class="da-btn da-btn-export">📥 Export <DownOutlined /></button>
        </a-dropdown>
      </div>
    </div>

    <div v-if="tripData" class="da-main-dashboard">
      <!-- Top Section: Overview & Map -->
      <div class="da-top-panel">
        <div class="da-overview-card">
          <h2 class="da-city-title">{{ tripData.city }} Adventure</h2>
          <p class="da-date-range">{{ tripData.start_date }} to {{ tripData.end_date }}</p>
          <p class="da-suggestions">{{ tripData.overall_suggestions }}</p>
          
          <!-- Budget -->
          <div v-if="tripData.budget" class="da-budget-grid">
            <div class="da-budget-item">
              <span class="da-b-label">Attractions</span>
              <span class="da-b-val">¥{{ tripData.budget.total_attractions }}</span>
            </div>
            <div class="da-budget-item">
              <span class="da-b-label">Hotels</span>
              <span class="da-b-val">¥{{ tripData.budget.total_hotels }}</span>
            </div>
            <div class="da-budget-item">
              <span class="da-b-label">Meals</span>
              <span class="da-b-val">¥{{ tripData.budget.total_meals }}</span>
            </div>
            <div class="da-budget-item">
              <span class="da-b-label">Transport</span>
              <span class="da-b-val">¥{{ tripData.budget.total_transportation }}</span>
            </div>
            <div class="da-budget-total">
              <span class="da-bt-label">Total Estimate</span>
              <span class="da-bt-val">¥{{ tripData.budget.total }}</span>
            </div>
          </div>
        </div>

        <div class="da-map-card">
          <div id="amap-container" class="da-map-container"></div>
        </div>
      </div>

      <!-- Itinerary Masonry -->
      <div class="da-itinerary-section">
        <h3 class="da-section-title">📅 Your Daily Itinerary</h3>
        
        <div class="da-days-container">
          <div v-for="(day, dIndex) in tripData.days" :key="dIndex" class="da-day-column">
            <div class="da-day-header">
              <h4>Day {{ day.day_index + 1 }}</h4>
              <span>{{ day.date }}</span>
            </div>
            
            <p class="da-day-desc">{{ day.description }}</p>
            <div class="da-day-meta">
              <span>🚗 {{ day.transportation }}</span>
              <span>🏨 {{ day.accommodation }}</span>
            </div>

            <!-- Attractions Masonry -->
            <div class="da-masonry-grid">
              <AttractionGlassCard
                v-for="(attr, aIndex) in day.attractions"
                :key="aIndex"
                :attraction="attr"
                :editMode="isEditing"
                :isFirst="aIndex === 0"
                :isLast="aIndex === day.attractions.length - 1"
                @moveUp="moveAttr(dIndex, aIndex, 'up')"
                @moveDown="moveAttr(dIndex, aIndex, 'down')"
                @delete="deleteAttr(dIndex, aIndex)"
              />
            </div>
            
            <!-- Hotel & Meals -->
            <div class="da-day-footer">
              <div v-if="day.hotel" class="da-hotel-info">
                <h5>🏨 {{ day.hotel.name }}</h5>
                <p>{{ day.hotel.address }}</p>
              </div>
              
              <div class="da-meals-info">
                <h5>🍽️ Meals</h5>
                <p v-for="(meal, mIndex) in day.meals" :key="mIndex">
                  <strong>{{ meal.type }}:</strong> {{ meal.name }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Weather Section -->
      <div v-if="tripData.weather_info && tripData.weather_info.length" class="da-weather-section">
        <h3 class="da-section-title">🌤️ Weather Forecast</h3>
        <div class="da-weather-grid">
          <WeatherGlassCard
            v-for="(w, wIndex) in tripData.weather_info"
            :key="wIndex"
            :weather="w"
          />
        </div>
      </div>
    </div>
    
    <div v-else class="da-empty-state">
      <div class="da-empty-icon">🗺️</div>
      <p>No trip plan found. Let's create one!</p>
      <button class="da-btn da-btn-primary" @click="goBack">Plan a Trip</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { DownOutlined } from '@ant-design/icons-vue'
import AMapLoader from '@amap/amap-jsapi-loader'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import type { TripPlan } from '@/types'
import WeatherGlassCard from '@/components/WeatherGlassCard.vue'
import AttractionGlassCard from '@/components/AttractionGlassCard.vue'

const router = useRouter()
const tripData = ref<TripPlan | null>(null)
const isEditing = ref(false)
const backupPlan = ref<TripPlan | null>(null)
let amapInstance: any = null

onMounted(async () => {
  const stored = sessionStorage.getItem('tripPlan')
  if (stored) {
    tripData.value = JSON.parse(stored)
    await nextTick()
    setupMap()
  }
})

const goBack = () => router.push('/')

const toggleEdit = () => {
  isEditing.value = true
  backupPlan.value = JSON.parse(JSON.stringify(tripData.value))
  message.info('Edit mode enabled')
}

const saveEdits = () => {
  isEditing.value = false
  if (tripData.value) {
    sessionStorage.setItem('tripPlan', JSON.stringify(tripData.value))
  }
  message.success('Changes saved')
  if (amapInstance) amapInstance.destroy()
  nextTick(() => setupMap())
}

const cancelEdits = () => {
  if (backupPlan.value) {
    tripData.value = JSON.parse(JSON.stringify(backupPlan.value))
  }
  isEditing.value = false
  message.info('Edits cancelled')
}

const moveAttr = (dayIdx: number, attrIdx: number, dir: 'up' | 'down') => {
  if (!tripData.value) return
  const list = tripData.value.days[dayIdx].attractions
  if (dir === 'up' && attrIdx > 0) {
    [list[attrIdx], list[attrIdx - 1]] = [list[attrIdx - 1], list[attrIdx]]
  } else if (dir === 'down' && attrIdx < list.length - 1) {
    [list[attrIdx], list[attrIdx + 1]] = [list[attrIdx + 1], list[attrIdx]]
  }
}

const deleteAttr = (dayIdx: number, attrIdx: number) => {
  if (!tripData.value) return
  const list = tripData.value.days[dayIdx].attractions
  if (list.length <= 1) {
    message.warning('At least one attraction required per day')
    return
  }
  list.splice(attrIdx, 1)
  message.success('Attraction removed')
}

const setupMap = async () => {
  try {
    const AMap = await AMapLoader.load({
      key: (import.meta as any).env.VITE_AMAP_WEB_JS_KEY || 'YOUR_KEY_HERE',
      version: '2.0',
      plugins: ['AMap.Marker', 'AMap.Polyline', 'AMap.InfoWindow']
    })

    amapInstance = new AMap.Map('amap-container', {
      zoom: 12,
      center: [116.397128, 39.916527],
      viewMode: '3D'
    })

    if (!tripData.value) return
    const markers: any[] = []
    const allLocs: any[] = []

    tripData.value.days.forEach((day, dIdx) => {
      day.attractions.forEach((attr, aIdx) => {
        if (attr.location?.longitude && attr.location?.latitude) {
          allLocs.push({ ...attr, dIdx, aIdx })
        }
      })
    })

    allLocs.forEach((attr, i) => {
      const marker = new AMap.Marker({
        position: [attr.location.longitude, attr.location.latitude],
        title: attr.name,
        label: {
          content: `<div style="background: var(--da-primary); color: white; padding: 4px 8px; border-radius: 8px;">${i + 1}</div>`,
          offset: new AMap.Pixel(0, -30)
        }
      })
      markers.push(marker)
    })

    amapInstance.add(markers)
    if (allLocs.length) amapInstance.setFitView(markers)
  } catch (err) {
    console.error('Map init failed:', err)
  }
}

const exportImage = async () => {
  try {
    message.loading({ content: 'Exporting...', key: 'export', duration: 0 })
    const el = document.querySelector('.da-main-dashboard') as HTMLElement
    if (!el) throw new Error('Content not found')
    
    const canvas = await html2canvas(el, {
      backgroundColor: '#f1f5f9',
      scale: 2,
      useCORS: true
    })
    
    const link = document.createElement('a')
    link.download = `AuraTrip_${tripData.value?.city}.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
    message.success({ content: 'Exported as Image!', key: 'export' })
  } catch (err: any) {
    message.error({ content: `Export failed: ${err.message}`, key: 'export' })
  }
}

const exportPdf = async () => {
  try {
    message.loading({ content: 'Exporting...', key: 'export', duration: 0 })
    const el = document.querySelector('.da-main-dashboard') as HTMLElement
    if (!el) throw new Error('Content not found')
    
    const canvas = await html2canvas(el, {
      backgroundColor: '#f1f5f9',
      scale: 2,
      useCORS: true
    })
    
    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')
    const w = 210
    const h = (canvas.height * w) / canvas.width
    let heightLeft = h
    let pos = 0
    
    pdf.addImage(imgData, 'PNG', 0, pos, w, h)
    heightLeft -= 297
    
    while (heightLeft > 0) {
      pos = heightLeft - h
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 0, pos, w, h)
      heightLeft -= 297
    }
    
    pdf.save(`AuraTrip_${tripData.value?.city}.pdf`)
    message.success({ content: 'Exported as PDF!', key: 'export' })
  } catch (err: any) {
    message.error({ content: `Export failed: ${err.message}`, key: 'export' })
  }
}
</script>

<style scoped>
.da-result-wrapper {
  max-width: 1600px;
  margin: 0 auto;
}

/* Header */
.da-header-glass {
  background: var(--da-bg-glass);
  backdrop-filter: blur(12px);
  border: 1px solid var(--da-border-glass);
  border-radius: 20px;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  box-shadow: var(--da-shadow-glass);
}

.da-btn {
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.da-btn-back {
  background: rgba(255,255,255,0.6);
  color: var(--da-text-main);
}
.da-btn-back:hover { background: rgba(255,255,255,0.8); }

.da-header-actions {
  display: flex;
  gap: 12px;
}

.da-btn-primary {
  background: var(--da-primary);
  color: white;
}
.da-btn-primary:hover { background: var(--da-primary-hover); }

.da-btn-edit { background: rgba(255,255,255,0.8); color: var(--da-text-main); }
.da-btn-cancel { background: #fef2f2; color: #ef4444; }
.da-btn-export { background: rgba(59, 130, 246, 0.1); color: var(--da-primary); }

/* Dashboard */
.da-main-dashboard {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* Top Panel */
.da-top-panel {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
}

.da-overview-card {
  flex: 1;
  min-width: 300px;
  background: var(--da-bg-glass);
  backdrop-filter: blur(16px);
  border: 1px solid var(--da-border-glass);
  border-radius: 24px;
  padding: 30px;
  box-shadow: var(--da-shadow-glass);
}

.da-city-title {
  font-size: 32px;
  font-weight: 800;
  color: var(--da-text-main);
  margin-bottom: 8px;
}

.da-date-range {
  font-size: 16px;
  color: var(--da-primary);
  font-weight: 600;
  margin-bottom: 20px;
}

.da-suggestions {
  color: var(--da-text-light);
  line-height: 1.6;
  margin-bottom: 30px;
  font-size: 15px;
}

.da-budget-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.da-budget-item {
  background: rgba(255,255,255,0.5);
  padding: 16px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.da-b-label { font-size: 13px; color: var(--da-text-light); }
.da-b-val { font-size: 18px; font-weight: 700; color: var(--da-text-main); }

.da-budget-total {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, var(--da-primary), #60a5fa);
  padding: 20px;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.da-bt-label { font-size: 16px; font-weight: 500; }
.da-bt-val { font-size: 24px; font-weight: 800; }

.da-map-card {
  flex: 1.5;
  min-width: 400px;
  background: var(--da-bg-glass);
  backdrop-filter: blur(16px);
  border: 1px solid var(--da-border-glass);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: var(--da-shadow-glass);
  min-height: 400px;
}

.da-map-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}

/* Itinerary */
.da-section-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--da-text-main);
  margin-bottom: 24px;
  padding-left: 12px;
  border-left: 4px solid var(--da-primary);
}

.da-days-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.da-day-column {
  background: var(--da-bg-glass);
  backdrop-filter: blur(16px);
  border: 1px solid var(--da-border-glass);
  border-radius: 24px;
  padding: 30px;
  box-shadow: var(--da-shadow-glass);
}

.da-day-header {
  display: flex;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 16px;
}

.da-day-header h4 {
  font-size: 28px;
  font-weight: 800;
  color: var(--da-primary);
  margin: 0;
}

.da-day-header span {
  font-size: 16px;
  color: var(--da-text-light);
  font-weight: 500;
}

.da-day-desc {
  font-size: 16px;
  color: var(--da-text-main);
  margin-bottom: 16px;
  line-height: 1.5;
}

.da-day-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  font-size: 14px;
  color: var(--da-text-light);
  background: rgba(255,255,255,0.4);
  padding: 12px 20px;
  border-radius: 12px;
  display: inline-flex;
}

.da-masonry-grid {
  column-count: 2;
  column-gap: 20px;
}

@media (max-width: 1000px) {
  .da-masonry-grid { column-count: 1; }
}

.da-day-footer {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.da-hotel-info, .da-meals-info {
  flex: 1;
  background: rgba(255,255,255,0.4);
  padding: 20px;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.3);
}

.da-hotel-info h5, .da-meals-info h5 {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--da-text-main);
}

.da-hotel-info p, .da-meals-info p {
  margin: 0 0 8px 0;
  color: var(--da-text-light);
  font-size: 14px;
}

/* Weather */
.da-weather-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.da-empty-state {
  text-align: center;
  padding: 100px 20px;
  background: var(--da-bg-glass);
  backdrop-filter: blur(16px);
  border-radius: 24px;
}

.da-empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.da-empty-state p {
  font-size: 18px;
  color: var(--da-text-light);
  margin-bottom: 30px;
}
</style>
