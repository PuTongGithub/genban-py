from ..tool import Tool
from src.hub.api.api_big_model import web_search
from src.common.utils.json_util import toJson

class WebSearchTool(Tool):
    
    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "联网搜索工具，用于搜索互联网上的实时信息。当对话主题具有实时性的时候务必使用。当对话内容中包含你不确定的信息时务必使用。"

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词，限制70个字符以内"
                },
                "count": {
                    "type": "integer",
                    "enum": [10, 20, 30, 40, 50],
                    "description": "返回结果数量，可选值为10、20、30、40、50，默认10"
                },
                "recency": {
                    "type": "string",
                    "enum": ["oneDay", "oneWeek", "oneMonth", "oneYear", "noLimit"],
                    "description": "时间过滤：oneDay(一天内)、oneWeek(一周内)、oneMonth(一个月内)、oneYear(一年内)、noLimit(不限，默认)"
                }
            },
            "required": ["query"]
        }

    def call(self, arguments: dict) -> str:
        query = arguments["query"]
        count = arguments.get("count", 10)
        recency = arguments.get("recency", "noLimit")
        result = web_search(
            search_query=query,
            count=count,
            search_recency_filter=recency
        )
        
        if "error" in result:
            return f"搜索失败：{result['error']}"
        
        search_results = result.get("search_result", [])
        if not search_results:
            return "搜索完成，但未找到相关结果"
        
        return toJson(search_results)
