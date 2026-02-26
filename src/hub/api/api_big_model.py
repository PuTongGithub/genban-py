import requests
from src.config.config import appConfig, envConfig

ZHIPU_WEB_SEARCH_URL = "https://open.bigmodel.cn/api/paas/v4/web_search"

def web_search(search_query: str, count: int = 10, search_recency_filter: str = "noLimit") -> dict:
    api_key = envConfig.get('ZHIPU_API_KEY')
    search_engine = appConfig.get("tools")["zhipu_search_engine"]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "search_query": search_query,
        "search_engine": search_engine,
        "count": count,
        "search_recency_filter": search_recency_filter,
        "content_size": "medium"
    }
    
    try:
        response = requests.post(ZHIPU_WEB_SEARCH_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"网络搜索请求失败: {str(e)}"}
    except Exception as e:
        return {"error": f"网络搜索发生错误: {str(e)}"}
