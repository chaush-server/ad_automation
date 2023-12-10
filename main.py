import asyncio
import json

import httpx

from login import login

url = "https://crm.lotinfo.ru/ajax/clients.php"
headers = {
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

client: httpx.AsyncClient = httpx.AsyncClient()


async def unpin(oid, sid):
    params = {
        "cmd": "advert",
        "oid": oid,
        "sid": sid,
        "c": "del",
    }
    response = await client.get(url, params=params, headers=headers)
    print(response.text)


async def pin(oid, sid):
    params = {
        "cmd": "advert",
        "oid": oid,
        "sid": sid,
        "c": "inAdv",
    }

    response = await client.get(url, params=params, headers=headers)
    print(
        "Выставлено"
        if response.text == "<input type=checkbox disabled checked>"
        else response.text
    )


async def check(oid):
    response = await client.get(
        f"https://crm.lotinfo.ru/object/{oid}", headers=headers
    )
    if "<font color=#FF0000><b>(архив)</b></font>" in response.text:
        return False
    return oid


async def remove_archives(oids):
    stack = [check(oid) for oid in oids]
    oids = [i for i in await asyncio.gather(*stack) if i]
    return oids


async def get_oids():
    oids = []
    with open("объекты.txt", "r", encoding="utf-8") as f:
        for line in f:
            oids.append(line.strip())
    return await remove_archives(oids)


async def user_choice(oids):
    ad_platforms = []
    with open("словарь_площадок.json", encoding="utf-8") as f:
        compare = json.loads(f.read())
    choose = input("Введите 1 для снятия, 2 для публикации: ")
    while choose not in ("1", "2"):
        print("Некорректный ввод")
        choose = input("Введите 1 для снятия, 2 для публикации: ")
    if choose == "1":
        file_name = "площадки_для_снятия.txt"
    else:
        file_name = "площадки_для_публикации.txt"

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            platform = line.strip()
            if platform:
                ad_platforms.append(platform)

    print(f"{oids} будут {'сняты' if choose == '1' else 'опубликованы'} в {ad_platforms}")
    if input("Продолжить? (y/n) ") != "y":
        exit()
    return (
        unpin if choose == "1" else pin,
        [compare[ad_platform] for ad_platform in ad_platforms]
    )


async def main():
    await login(client)
    oids = await get_oids()
    task, ad_platforms = await user_choice(oids)
    corutines = [task(oid, ad_platform) for oid in oids for ad_platform in ad_platforms]
    while corutines:
        await asyncio.gather(*corutines[:10])
        await asyncio.sleep(0.5)
        corutines = corutines[10:]


if __name__ == "__main__":
    asyncio.run(main())
    input("Нажмите Enter для выхода")
