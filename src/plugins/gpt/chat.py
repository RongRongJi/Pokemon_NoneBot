import requests


def chat(content):
    try:
        headers = {
        'Content-Type':'application/json'
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages":[{"role":"user", "content": content}]
        }

        response = requests.post('https://chatgpt-api.shn.hk/v1/', headers=headers, json=data)
        print(response)
        ret = response.json()
        
        return ret['choices'][0]['message']['content'].lstrip()
    except Exception as e:
        print(e)
        return '听不懂, 我开摆了'