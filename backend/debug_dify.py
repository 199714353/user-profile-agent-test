import asyncio
import httpx
import json

async def test():
    api_key = "app-33QFU9RLluraZy9P92lDGjHc"
    url = "https://api.dify.ai/v1/workflows/run"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {
            "pinglun": "动力很好的车"
        },
        "response_mode": "blocking",
        "user": "test_user"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))

asyncio.run(test())
