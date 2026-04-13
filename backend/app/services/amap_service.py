"""高德地图MCP服务封装"""


from typing import List,Dict, Any, Optional
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from ..config import get_settings
from ..models.schemas import Location, POIInfo, WeatherInfo



# 全局MCP工具实例
_amap_mcp_tool = None
_mcp_client = None

def get_amap_mcp_tool():
    """获取高德地图MCP工具实例(单例模式)"""
    global _amap_mcp_tool, _mcp_client
    
    if _amap_mcp_tool is None:
        settings = get_settings()
        
        if not settings.amap_api_key:
            raise ValueError("高德地图API Key未配置,请在.env文件中设置AMAP_API_KEY")
            
        # 使用 LangChain MCP 适配器创建客户端
        _mcp_client = MultiServerMCPClient({
            "amap": {
                "command": "uvx",
                "args": ["amap-mcp-server"],
                "env": {"AMAP_MAPS_API_KEY": settings.amap_api_key},
                "transport": "stdio",
            }
        })
        
        # 获取工具
        _amap_mcp_tool = asyncio.run(_mcp_client.get_tools())
        print(f"高德地图MCP工具初始化成功 (LangChain/LangGraph)")
        
    return _amap_mcp_tool


class AmapService:
    """高德地图服务封装类"""
    
    def __init__(self):
        """初始化服务"""
        self.mcp_tool = get_amap_mcp_tool()

    def search_poi(self, keywords: str, city: str, citylimit: bool = True) -> list[POIInfo]:
        """
        搜索POI
        
        Args:
            keywords: 搜索关键词
            city: 城市
            citylimit: 是否限制在城市范围内
            
        Returns:
            POI信息列表
        """
        try:
            # 在MCP工具列表中查找 maps_text_search 工具
            tool = next((t for t in self.mcp_tool if t.name == "maps_text_search"), None)
            if not tool:
                print("未找到 maps_text_search 工具")
                return []
                
            # 调用MCP工具
            result = tool.invoke({
                "keywords": keywords,
                "city": city,
                "citylimit": str(citylimit).lower()
            })
            
            # 打印部分结果便于调试
            print(f"POI搜索结果: {str(result)[:200]}...")
            
            # TODO: 解析实际的POI数据
            return []
            
        except Exception as e:
            print(f"搜索POI失败: {e}")
            return []
        
    def get_weather(self, city: str) -> List[WeatherInfo]:
        """
        查询天气
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息列表
        """
        try:
            # 在MCP工具列表中查找 maps_weather 工具
            tool = next((t for t in self.mcp_tool if t.name == "maps_weather"), None)
            if not tool:
                print("未找到 maps_weather 工具")
                return []
                
            # 调用MCP工具
            result = tool.invoke({
                "city": city
            })
            
            print(f"天气查询结果: {str(result)[:200]}...")
            
            # TODO: 解析实际的天气数据
            return []
            
        except Exception as e:
            print(f"❌ 天气查询失败: {str(e)}")
            return []

    def plan_route(
        self,
        origin_address: str,
        destination_address: str,
        origin_city: Optional[str] = None,
        destination_city: Optional[str] = None,
        route_type: str = "walking"
    ) -> Dict[str, Any]:
        """
        规划路线
        
        Args:
            origin_address: 起点地址
            destination_address: 终点地址
            origin_city: 起点城市
            destination_city: 终点城市
            route_type: 路线类型 (walking/driving/transit)
            
        Returns:
            路线信息
        """
        try:
            # 根据路线类型选择工具
            tool_map = {
                "walking": "maps_direction_walking_by_address",
                "driving": "maps_direction_driving_by_address",
                "transit": "maps_direction_transit_integrated_by_address"
            }
            
            tool_name = tool_map.get(route_type, "maps_direction_walking_by_address")
            
            # 在MCP工具列表中查找对应工具
            tool = next((t for t in self.mcp_tool if t.name == tool_name), None)
            if not tool:
                print(f"未找到 {tool_name} 工具")
                return {}
            
            # 构建参数
            arguments = {
                "origin_address": origin_address,
                "destination_address": destination_address
            }
            
            # 公共交通需要城市参数
            if route_type == "transit":
                if origin_city:
                    arguments["origin_city"] = origin_city
                if destination_city:
                    arguments["destination_city"] = destination_city
            else:
                # 其他路线类型也可以提供城市参数提高准确性
                if origin_city:
                    arguments["origin_city"] = origin_city
                if destination_city:
                    arguments["destination_city"] = destination_city
            
            # 调用MCP工具
            result = tool.invoke(arguments)
            
            print(f"路线规划结果: {str(result)[:200]}...")
            
            # TODO: 解析实际的路线数据
            return {}
            
        except Exception as e:
            print(f"❌ 路线规划失败: {str(e)}")
            return {}
    
    def geocode(self, address: str, city: Optional[str] = None) -> Optional[Location]:
        """
        地理编码(地址转坐标)

        Args:
            address: 地址
            city: 城市

        Returns:
            经纬度坐标
        """
        try:
            tool = next((t for t in self.mcp_tool if t.name == "maps_geo"), None)
            if not tool:
                print("未找到 maps_geo 工具")
                return None

            arguments = {"address": address}
            if city:
                arguments["city"] = city

            result = tool.invoke(arguments)

            print(f"地理编码结果: {str(result)[:200]}...")

            # TODO: 解析实际的坐标数据
            return None

        except Exception as e:
            print(f"❌ 地理编码失败: {str(e)}")
            return None

    def get_poi_detail(self, poi_id: str) -> Dict[str, Any]:
        """
        获取POI详情

        Args:
            poi_id: POI ID

        Returns:
            POI详情信息
        """
        try:
            tool = next((t for t in self.mcp_tool if t.name == "maps_search_detail"), None)
            if not tool:
                print("未找到 maps_search_detail 工具")
                return {}

            result = tool.invoke({
                "id": poi_id
            })

            print(f"POI详情结果: {str(result)[:200]}...")

            # 解析结果并提取图片
            import json
            import re

            # 尝试从结果中提取JSON
            result_str = str(result)
            json_match = re.search(r'\{.*\}', result_str, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data

            return {"raw": result_str}

        except Exception as e:
            print(f"❌ 获取POI详情失败: {str(e)}")
            return {}


# 创建全局服务实例
_amap_service = None

def get_amap_service() -> AmapService:
    """获取高德地图服务实例(单例模式)"""
    global _amap_service
    
    if _amap_service is None:
        _amap_service = AmapService()
    
    return _amap_service

# if __name__ == "__main__":
#     import sys
#     import os
    
#     # 将 backend 目录添加到 sys.path 以便直接运行测试
#     backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     if backend_dir not in sys.path:
#         sys.path.insert(0, backend_dir)
        
#     try:
#         print("正在初始化高德地图 MCP 工具...")
#         tools = get_amap_mcp_tool()
#         print(f"\n成功获取到 {len(tools)} 个工具:")
#         for tool in tools:
#             print(f" - {tool.name}: {tool.description}")
#     except Exception as e:
#         print(f"测试失败: {e}")