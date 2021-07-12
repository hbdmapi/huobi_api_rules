import requests
from urllib import parse
import json
from datetime import datetime
import hmac
import base64
from hashlib import sha256


def _get_url_suffix(method: str, access_key: str, secret_key: str, host: str, path: str) -> str:
    # it's utc time and an example is 2017-05-11T15:19:30
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    timestamp = parse.quote(timestamp)  # url encode
    suffix = 'AccessKeyId={}&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp={}'.format(
        access_key, timestamp)
    payload = '{}\n{}\n{}\n{}'.format(method.upper(), host, path, suffix)

    digest = hmac.new(secret_key.encode('utf8'), payload.encode(
        'utf8'), digestmod=sha256).digest()  # make sha256 with binary data

    # base64 encode with binary data and then get string
    signature = base64.b64encode(digest).decode()
    signature = parse.quote(signature)  # url encode

    suffix = '{}&Signature={}'.format(suffix, signature)
    return suffix


def get(access_key: str, secret_key: str, host: str, path: str, params: dict = None) -> json:
    try:
        url = 'https://{}{}?{}'.format(host, path, _get_url_suffix(
            'get', access_key, secret_key, host, path))
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        # params are parts of url path
        res = requests.get(url, params=params, headers=headers)
        data = res.json()
        return data
    except Exception as e:
        logger.error(e)
    return None


def post(access_key: str, secret_key: str, host: str, path: str, data: dict = None) -> json:
    try:
        url = 'https://{}{}?{}'.format(host, path, _get_url_suffix(
            'post', access_key, secret_key, host, path))
        headers = {'Accept': 'application/json',
                   'Content-type': 'application/json'}
        # json means data with json format string in http body
        res = requests.post(url, json=data, headers=headers)
        data = res.json()
        return data
    except Exception as e:
        logger.error(e)
    return None


if __name__ == '__main__':
    access_key = 'xxx'
    secret_key = 'xxx'

    # spot
    host = 'api.huobi.pro'
    path = '/v1/account/accounts'
    acc_json = get(access_key, secret_key, host, path, None)
    aid = None
    for item in acc_json['data']:
        if item['type'] == 'spot':
            aid = item['id']
            break
    if aid is not None:
        path = '/v1/account/accounts/{}/balance'.format(aid)
        print('spot:{}\n'.format(get(access_key, secret_key, host, path, None)))

    # future
    host = 'api.hbdm.vn'
    path = '/api/v1/contract_position_info'
    params = {'symbol': 'btc'}
    print('future:{}\n'.format(post(access_key, secret_key, host, path, params)))

    # coin-swap
    host = 'api.hbdm.vn'
    path = '/swap-api/v1/swap_position_info'
    params = {'contract_code': 'btc-usd'}
    print('coin-swap:{}\n'.format(post(access_key, secret_key, host, path, params)))

    # usdt-swap
    host = 'api.hbdm.vn'
    path = '/linear-swap-api/v1/swap_cross_position_info'
    params = {'contract_code': 'btc-usdt'}
    print('usdt-swap:{}\n'.format(post(access_key, secret_key, host, path, params)))
