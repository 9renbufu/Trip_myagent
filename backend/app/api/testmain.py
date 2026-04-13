from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import TripRequest, TripPlan, TripPlanResponse

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，开发环境适用。生产环境应指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，包括 OPTIONS
    allow_headers=["*"],
)

@app.post("/api/trip/plan", response_model=TripPlanResponse)
async def create_trip_plan(request: TripRequest) -> TripPlanResponse:
    """
    创建旅行计划
    
    FastAPI自动：
    1. 验证请求数据(TripPlanRequest)
    2. 验证响应数据(TripPlanResponse)
    3. 生成OpenAPI文档
    """
    # 模拟数据
    mock_plan = TripPlan(
        city=request.city,
        start_date=request.start_date.strftime("%Y-%m-%d"),
        end_date=request.end_date.strftime("%Y-%m-%d"),
        days=[],
        weather_info=[],
        overall_suggestions="这是一个测试旅行计划建议"
    )
    
    return TripPlanResponse(
        success=True,
        message="计划生成成功",
        data=mock_plan
    )
