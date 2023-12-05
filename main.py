import httpx

compare = {
    "": "0",
    "www.avito.ru": "27",
    "Сайт компании": "37",
    "Яндекс Недвижимость": "56",
    "cian.ru": "72",
    "квартиры-домики.рф": "81",
    "realtymag.ru": "94",
    'East Estate "Восточная недвижимость"': "109",
    "radver.ru": "112",
    "e64.ru": "118",
    "rucountry.ru": "121",
    "russianrealty.ru": "124",
    "mlspro.ru": "148",
    "allpn.ru": "196",
    "move.ru": "220",
    "naydidom.com": "251",
    "mesto.ru": "255",
    "domex.ru": "259",
    "gde.ru": "301",
    "reforum.ru": "326",
    "gdeetotdom.ru": "331",
    "1pbn.ru": "336",
    "glavbaza.su": "361",
    "rusnedviga.ru": "455",
    "Сбербанк": "470",
    "IMLS.RU": "540",
    "house2you.ru": "579",
    "multilisting.su": "605",
    "domoved.su": "635",
    "moyareklama.ru": "679",
    "unibo.ru": "1589",
    "youla": "1707",
    "cmlt.ru": "1712",
    "www.remospro.ru": "1732",
    "gorodkvadratov.ru": "1749",
    "realtybell.ru": "2704",
    "alsibo.com": "2987",
    "m2.ru": "3095",
    "ligakvartir.ru": "3154",
    "m-sq.ru": "3263",
    "atuta.ru": "3373",
}
cookies = {
    "uid": "9175",
    "auth_cookie": "47ecf4da9891899e892faecde82700fd",
    "secure_key_newmain": "946db9c9c836d4539e61c3300fd26e1f",
}
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}
url = "https://crm.lotinfo.ru/ajax/clients.php"
client = httpx.Client()


def unpin(oid, sid):
    params = {
        "cmd": "advert",
        "oid": oid,
        "sid": sid,
        "c": "del",
    }
    response = client.get(url, params=params, cookies=cookies, headers=headers)
    print(response.text)


def pin(oid, sid):
    params = {
        "cmd": "advert",
        "oid": "552337",
        "sid": "37",
        "c": "inAdv",
    }

    response = client.get(url, params=params, cookies=cookies, headers=headers)
    print("Выставлено" if response.text == "<input type=checkbox disabled checked>" else response.text)


def check(oid):
    response = client.get(f"https://crm.lotinfo.ru/object/{oid}", cookies=cookies, headers=headers)
    if "<font color=#FF0000><b>(архив)</b></font>" in response.text:
        return False
    return True


def main():
    check(522463)

    # unpin(552337, 37)
    # pin(552337, 37)
    oids = []
    with open("объекты.txt", "r", encoding="utf-8") as f:
        for line in f:
            oids.append(line.strip())

    snames = []
    while (choose := input("Введите 1 для снятия, 2 для публикации: ")) not in ("1", "2"):
        print("Такого варианта нет")
        continue

    if choose == "1":
        file_name = "площадки_для_снятия.txt"
    else:
        file_name = "площадки_для_публикации.txt"

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            snames.append(line.strip())

    print(f"{oids} будут {'сняты' if choose == '1' else 'опубликованы'} в {snames}")
    if input("Продолжить? (y/n) ") != "y":
        exit()

    func = unpin if choose == "1" else pin
    for oid in oids:
        for sname in snames:
            if check(oid):
                func(oid, compare[sname])
            else:
                print(f"{oid} в архиве")


if __name__ == "__main__":
    main()
