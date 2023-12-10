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


async def unpin(oid, sid):
    params = {
        "cmd": "advert",
        "oid": oid,
        "sid": sid,
        "c": "del",
    }
    if not await check(oid):
        return print("Архив", oid)

    response = await client.get(url, params=params, headers=headers)
    print(response.text if response.text == "Снято" else 'Не снято' + response.text)


async def pin(oid, sid):
    params = {
        "cmd": "advert",
        "oid": oid,
        "sid": sid,
        "c": "inAdv",
    }
    if not await check(oid):
        return print("Архив", oid)
    response = await client.get(url, params=params, headers=headers)
    if response.text == "<input type=checkbox disabled checked>":
        print("Выставлено")
    else:
        print("Не выставлено" + response.text)
        await unpin(oid, sid)


async def check(oid):
    response = await client.get(
        f"https://crm.lotinfo.ru/object/{oid}", headers=headers
    )
    if "<font color=#FF0000><b>(архив)</b></font>" in response.text:
        return False
    return True


# async def remove_archives(oids):
#     tasks = [check(oid) for oid in oids]
#     result = []
#     while tasks:
#         result.extend([i for i in await asyncio.gather(*tasks[:1000]) if i])
#         print(len(tasks))
#         tasks = tasks[1000:]
#     return [i for i in result if i]


async def get_oids():
    oids = []
    with open("объекты.txt", "r", encoding="utf-8-sig") as f:
        oids.extend(f.read().split())
    return oids


async def user_choice(oids):
    ad_platforms = []
    with open("словарь_площадок.json", encoding="utf-8-sig") as f:
        compare = json.loads(f.read())
    choose = input("Введите 1 для снятия, 2 для публикации: ")
    while choose not in ("1", "2"):
        print("Некорректный ввод")
        choose = input("Введите 1 для снятия, 2 для публикации: ")
    if choose == "1":
        file_name = "площадки_для_снятия.txt"
    else:
        file_name = "площадки_для_публикации.txt"
    with open(file_name, "r", encoding="utf-8-sig") as f:
        for line in f:
            platform = line.strip()
            if platform:
                ad_platforms.append(platform)

    print(f"{oids[:10]} будут {'сняты' if choose == '1' else 'опубликованы'} в {ad_platforms}")
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
        await asyncio.sleep(.5)
        corutines = corutines[10:]


if __name__ == "__main__":
    client: httpx.AsyncClient = httpx.AsyncClient()
    asyncio.run(main())
    input("Нажмите Enter для выхода")
