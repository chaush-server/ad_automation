import httpx


async def login(client: httpx.AsyncClient):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    data = {
        'form[signup]': '1',
        'form[phone]': '+7 952 804 67 35',
        'form[pass]': 'Mgrasnast100',
        'form[ajax]': '1',
    }
    await client.post("https://lotinfo.ru/auth", data=data, headers=headers)
    await client.get("https://crm.lotinfo.ru/?main", headers=headers)
