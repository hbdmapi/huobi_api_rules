import requests
import json


def get(host: str, path: str, params: dict = None) -> json:
    try:
        url = 'https://{}{}'.format(host, path)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        
        # params are parts of url path
        res = requests.get(url, params=params, headers=headers)
        data = res.json()
        return data
    except Exception as e:
        logger.error(e)
    return None


if __name__ == '__main__':
    # spot
    host = 'api.huobi.pro'
    path = '/market/history/kline'
    params = {'period': '1day', 'size': 2, 'symbol': 'btcusdt'}
    print('spot:{}\n'.format(get(host, path, params)))

    # future
    host = 'api.hbdm.vn'
    path = '/market/history/kline'
    params = {'period': '1day', 'size': 2, 'symbol': 'btc_cq'}
    print('future:{}\n'.format(get(host, path, params)))

    # coin-swap
    host = 'api.hbdm.vn'
    path = '/swap-ex/market/history/kline'
    params = {'period': '1day', 'size': 2, 'contract_code': 'btc-usd'}
    print('coin-swap:{}\n'.format(get(host, path, params)))

    # usdt-swap
    host = 'api.hbdm.vn'
    path = '/linear-swap-ex/market/history/kline'
    params = {'period': '1day', 'size': 2, 'contract_code': 'btc-usdt'}
    print('usdt-swap:{}\n'.format(get(host, path, params)))
