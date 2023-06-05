import httpx
import json

async def chat_gpt_async(message, chat_context):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer MEU_TOKEN_API',
        'Content-Type': 'application/json'
    }

    data = {
    'messages': chat_context['messages'] + [
        {'role': 'user', 'content': message}
    ],
    'model': 'gpt-3.5-turbo'
}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

    response_json = response.json()
    if 'choices' in response_json:
        retornoApi = response_json['choices'][0]['message']['content']
        return retornoApi
    else:
        return None