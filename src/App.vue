<template>
  <div id="da-planner-app">
    <a-layout class="da-layout-root">
      <a-layout-header class="da-glass-header">
        <div class="da-logo">
          <span class="da-logo-icon">✨</span>
          <span class="da-logo-text">AuraTrip Planner</span>
        </div>
      </a-layout-header>
      
      <a-layout-content class="da-main-content">
        <router-view />
      </a-layout-content>
      
      <a-layout-footer class="da-glass-footer">
        <div class="signature">Developed by da]</div>
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
:root {
  --da-primary: #3B82F6;
  --da-primary-hover: #2563EB;
  --da-bg-glass: rgba(255, 255, 255, 0.25);
  --da-border-glass: rgba(255, 255, 255, 0.18);
  --da-shadow-glass: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
  --da-text-main: #1e293b;
  --da-text-light: #475569;
}

body {
  margin: 0;
  padding: 0;
  background-color: #f1f5f9;
  background-image: radial-gradient(at 40% 20%, hsla(228,100%,74%,1) 0px, transparent 50%),
                    radial-gradient(at 80% 0%, hsla(189,100%,56%,1) 0px, transparent 50%),
                    radial-gradient(at 0% 50%, hsla(355,100%,93%,1) 0px, transparent 50%);
  background-attachment: fixed;
  min-height: 100vh;
}

#da-planner-app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
}

.da-layout-root {
  background: transparent !important;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.da-glass-header {
  background: var(--da-bg-glass) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--da-border-glass);
  padding: 0 40px !important;
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}

.da-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.da-logo-icon {
  font-size: 28px;
}

.da-logo-text {
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--da-primary), #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.da-main-content {
  flex: 1;
  padding: 30px 40px;
}

.da-glass-footer {
  background: var(--da-bg-glass) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-top: 1px solid var(--da-border-glass);
  text-align: center;
  padding: 20px !important;
  color: var(--da-text-light);
  font-size: 14px;
  letter-spacing: 1px;
}

.signature {
  font-weight: 600;
  color: var(--da-primary);
  text-shadow: 0 1px 2px rgba(255,255,255,0.8);
}
</style>
