# Trip Planner Agent (旅游规划助手)

这是一个基于大语言模型（LLM）和多智能体（Multi-Agent）合作的旅游规划助手。它可以帮助用户自动生成详细的旅行计划、搜索周边景点（POI）、查询天气以及获取景点相关图片。

## 🌟 核心功能

*   **智能行程规划**：基于 LLM 自动生成每日的旅行路线与时间安排。
*   **地图与POI服务**：集成高德地图（Amap）API，提供准确的地点搜索、路径规划及天气查询。
*   **美图展示**：集成 Unsplash API，为景点和城市提供高质量的展示图片。
*   **现代化 UI**：提供美观、响应式的 Vue 3 前端界面。

## 📂 项目结构

项目主要包含两大部分：

*   **`frontend/`**: 前端项目，基于 Vue 3 + TypeScript + Vite 构建。主要用于展示行程、景点信息及交互界面。
*   **`backend/`**: 后端项目，基于 Python 和 FastAPI 框架构建。包含 API 路由、基于 LangChain 和 LangGraph 构建的 Agent 逻辑，以及第三方服务接入（高德地图、大模型、Unsplash）。

## 🚀 快速开始

### 1. 后端服务 (Backend)

1. 进入后端目录：
   ```bash
   cd backend
   ```
2. 安装依赖 (推荐使用虚拟环境，假设存在 `requirements.txt`)：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量：
   在 `backend` 目录下创建或编辑 `.env` 文件，并参考相关配置填入您的 API Key：
   ```env
   # LLM API Key
   LLM_API_KEY=your_api_key_here
   # 高德地图 API Key
   AMAP_API_KEY=your_amap_key_here
   # Unsplash API Key
   UNSPLASH_API_KEY=your_unsplash_key_here
   ```
4. 启动后端服务：
   ```bash
   python run.py
   ```

### 2. 前端服务 (Frontend)

1. 进入前端目录：
   ```bash
   cd frontend
   ```
2. 安装依赖：
   ```bash
   npm install
   ```
3. 配置环境变量：
   在 `frontend` 目录下复制 `.env.example` 为 `.env`，并配置后端接口地址等信息。
4. 启动开发服务器：
   ```bash
   npm run dev
   ```

## 🛠️ 技术栈

*   **前端**：Vue 3, TypeScript, Vite
*   **后端**：Python, FastAPI, LangChain, LangGraph
*   **第三方服务**：高德地图 API, Unsplash API, LLM API

---

*本项目为一个简单的多智能体合作完成的旅游规划助手实例。*
