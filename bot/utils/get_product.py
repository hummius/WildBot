from typing import Dict

import requests


URL = 'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm='


async def get_product_info(vendor_code: Dict) -> Dict:
    response = requests.request(method="GET", url=f'{URL+vendor_code["code"]}', timeout=20)
    resp = response.json()['data']['products'][0]
    query = {
        'name': resp['name'],
        'id': resp['id'],
        'price': resp['salePriceU'],
        'rating': resp['reviewRating'],
        'stocks': resp['sizes'][0]['stocks']
    }
    return query


async def get_info(vendor_code: Dict) -> str:
    info = await get_product_info(vendor_code)
    qty = [wh['qty'] for wh in info['stocks']]
    template = (f'<b>👉 Имя: {info["name"]}</b>\n'
                f'<b>👉 Артикул: {info["id"]}</b>\n'
                f'<b>👉 Цена: {round(info["price"]/100, 2)}р.</b>\n'
                f'<b>👉 Рейтинг: {info["rating"]}</b>\n'
                f'<b>👉 Кол-во на складах: {qty}</b>\n')
    return template
