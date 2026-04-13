from typing import List, Optional, Any, Sequence
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph

class SimpleAgent:
    """基于 LangGraph create_react_agent 封装的简单智能体"""
    
    def __init__(
        self,
        name: str,
        llm: BaseChatModel,
        system_prompt: Optional[str] = None,
        tools: Optional[Sequence[BaseTool]] = None
    ):
        """
        初始化 SimpleAgent
        
        Args:
            name: Agent名称
            llm: LangChain 的 ChatModel 实例 (如 ChatOpenAI)
            system_prompt: 系统提示词
            tools: 可供 Agent 调用的 LangChain 工具列表
        """
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt or "你是一个有用的 AI 助手。"
        self.tools = tools or []
        
        # 使用 LangGraph 内置的 create_react_agent 快速创建一个支持工具调用的 ReAct Agent
        self.agent: CompiledStateGraph = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=self.system_prompt
        )

    def add_tool(self, tool: BaseTool):
        """动态添加工具，注意：添加工具后需要重新编译 agent"""
        if isinstance(tool, list):
            self.tools.extend(tool)
        else:
            self.tools.append(tool)
            
        # 重新编译 agent 以包含新工具
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=self.system_prompt
        )
        
    def add_tools(self, tools: Sequence[BaseTool]):
        """批量添加工具"""
        self.tools.extend(tools)
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=self.system_prompt
        )

    def run(self, query: str) -> str:
        """
        运行 Agent 并获取最终回复 (同步调用)
        
        Args:
            query: 用户输入的问题
            
        Returns:
            Agent 的最终回答文本
        """
        messages = [HumanMessage(content=query)]
        
        # 调用 compiled graph
        response_state = self.agent.invoke({"messages": messages})
        
        # 返回最后一条消息的内容
        return response_state["messages"][-1].content
        
    async def arun(self, query: str) -> str:
        """
        异步运行 Agent
        """
        messages = [HumanMessage(content=query)]
        response_state = await self.agent.ainvoke({"messages": messages})
        return response_state["messages"][-1].content

    def list_tools(self) -> List[str]:
        """获取当前 Agent 拥有的工具名称列表"""
        return [tool.name for tool in self.tools]