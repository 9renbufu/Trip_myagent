
"""LLM服务模块"""
import os
from langchain_openai import ChatOpenAI
from ..config import get_settings

# 全局LLM实例
_llm_instance = None

def get_llm() -> ChatOpenAI:
    """
    获取LLM实例(单例模式) - 使用 LangChain 
    Returns:
        ChatOpenAI实例
    """
    global _llm_instance
    
    if _llm_instance is None:
        settings = get_settings()
        
        # 优先从环境变量获取，如果为空则使用 settings 里的配置
        api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY") or settings.openai_api_key
        base_url = os.getenv("LLM_BASE_URL") or settings.openai_base_url
        model_name = os.getenv("LLM_MODEL_ID") or settings.openai_model
        
        # 为了兼容不同的服务商（比如 qwen 也可以通过 openai 接口兼容），这里使用 ChatOpenAI
        _llm_instance = ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=base_url,
            model_name=model_name,
            temperature=0.7,  # 可根据需要调整
        )
        
        print(f"✅ LLM服务初始化成功 (基于 LangChain)")
        print(f"   Base URL: {base_url}")
        print(f"   模型: {model_name}")
    
    return _llm_instance

def reset_llm():
    """重置LLM实例(用于测试或重新配置)"""
    global _llm_instance
    _llm_instance = None

# if __name__ == "__main__":
#     get_llm()
#     print(get_llm().invoke("你好"))
#     print("LLM服务测试通过")