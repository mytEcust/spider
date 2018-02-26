"""
每天自动获取机票最低价并发送至邮箱
"""
# -*- coding: utf-8 -*-
from configobj import ConfigObj

import asyncio
import aiohttp
import json

BIG_NUM = 9999999

CF = ConfigObj('./config/travel.conf')

API_URL = CF['api']['url']
BROWSE_ROUTES = CF['api']['browseroutes']
DETAIL_URL = CF['api']['detailurl']
API_KEY = CF['api']['apikey']
COUNTRY = CF['args']['country']
CURRENCY = CF['args']['currency']
LOCALE = CF['args']['locale']
TRIPS = CF['args']['trips']

BROWSE_ROUTES = BROWSE_ROUTES.format(
    country=COUNTRY, currency=CURRENCY, locale=LOCALE)

trips = []
for trip in TRIPS:
    originPlace = CF['args']['trips'][trip]['originPlace']
    destinationPlace = CF['args']['trips'][trip]['destinationPlace']
    outboundPartialDate = CF['args']['trips'][trip]['outboundPartialDate']
    inboundPartialDate = CF['args']['trips'][trip]['inboundPartialDate']
    direct = CF['args']['trips'][trip]['direct']
    url = DETAIL_URL.format(
        originPlace=originPlace,
        destinationPlace=destinationPlace,
        outboundPartialDate=outboundPartialDate,
        inboundPartialDate=inboundPartialDate,
        apikey=API_KEY
    )
    trips.append({
        'url': API_URL+BROWSE_ROUTES+url,
        'direct': direct
    })

print(trips)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_trip(api_url, direct):
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, api_url)
        result = json.loads(result)
        min_price = BIG_NUM
        carrier_id = ''
        carrier_name = ''
        print(result)
        for quote in result['Quotes']:
            if direct == 'true':
                if quote['Direct'] is False:
                    continue
            if quote['MinPrice'] < min_price:
                min_price = quote['MinPrice']
                carrier_id = quote['OutboundLeg']['CarrierIds'][0]

        if min_price == BIG_NUM:
            raise NameError('没有获取到机票价格')

        for carrier in result['Carriers']:
            if carrier['CarrierId'] == carrier_id:
                carrier_name=carrier['Name']

        print(min_price,carrier_name)


def get_all_trips(trips):
    promise = []
    loop = asyncio.get_event_loop()
    for trip in trips:
        promise.append(get_trip(trip['url'], trip['direct']))
    loop.run_until_complete(asyncio.wait(promise))
    loop.close()

try:
    get_all_trips(trips)
except Exception as err:
    print('err')
