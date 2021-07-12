import websocket
import threading
import time
import json
import gzip
from datetime import datetime
from urllib import parse
import hmac
import base64
from hashlib import sha256


class Ws:
    def __init__(self, host: str, path: str, access_key: str, secret_key: str, be_spot: bool):
        self._host = host
        self._path = path
        self._access_key = access_key
        self._secret_key = secret_key
        self._be_spot = be_spot
        self._active_close = False
        self._has_open = False
        self._sub_str = None
        self._ws = None

    def open(self):
        url = 'wss://{}{}'.format(self._host, self._path)
        self._ws = websocket.WebSocketApp(url,
                                          on_open=self._on_open,
                                          on_message=self._on_msg,
                                          on_close=self._on_close,
                                          on_error=self._on_error)
        t = threading.Thread(target=self._ws.run_forever, daemon=True)
        t.start()

    def _on_open(self, ws):
        print('ws open')
        signature_data = self._get_signature_data()  # signature data
        self._ws.send(json.dumps(signature_data))  # as json string to be send
        self._has_open = True

    def _get_signature_data(self) -> dict:
        # it's utc time and an example is 2017-05-11T15:19:30
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        url_timestamp = parse.quote(timestamp)  # url encode

        # get Signature
        if self._be_spot:
            suffix = 'accessKey={}&signatureMethod=HmacSHA256&signatureVersion=2.1&timestamp={}'.format(
                access_key, url_timestamp)
        else:
            suffix = 'AccessKeyId={}&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp={}'.format(
                access_key, url_timestamp)
        payload = '{}\n{}\n{}\n{}'.format('GET', host, path, suffix)

        digest = hmac.new(self._secret_key.encode('utf8'), payload.encode(
            'utf8'), digestmod=sha256).digest()  # make sha256 with binary data
        # base64 encode with binary data and then get string
        signature = base64.b64encode(digest).decode()

        # data
        if self._be_spot:
            data = {
                "action": "req",
                "ch": "auth",
                "params": {
                    "authType": "api",
                    "accessKey": self._access_key,
                    "signatureMethod": "HmacSHA256",
                    "signatureVersion": "2.1",
                    "timestamp": timestamp,
                    "signature": signature
                }
            }
        else:
            data = {
                "op": "auth",
                "type": "api",
                "AccessKeyId": self._access_key,
                "SignatureMethod": "HmacSHA256",
                "SignatureVersion": "2",
                "Timestamp": timestamp,
                "Signature": signature
            }
        return data

    def _on_msg(self, ws, message):
        plain = message
        if not self._be_spot:
            plain = gzip.decompress(message).decode()
        
        jdata = json.loads(plain)
        if 'ping' in jdata:
            sdata = plain.replace('ping', 'pong')
            self._ws.send(sdata)
            return
        elif 'op' in jdata:
            opdata = jdata['op']
            if opdata == 'ping':
                sdata = plain.replace('ping', 'pong')
                self._ws.send(sdata)
                return
            else:
                pass
        elif 'action' in jdata:
            opdata = jdata['action']
            if opdata == 'ping':
                sdata = plain.replace('ping', 'pong')
                self._ws.send(sdata)
                return
            else:
                pass
        else:
            pass
        print(jdata)

    def _on_close(self, ws):
        print("ws close.")
        self._has_open = False
        if not self._active_close and self._sub_str is not None:
            self._create_ws()
            self.sub(self._sub_str)

    def _on_error(self, ws, error):
        print(error)

    def sub(self, sub_str: dict):
        if self._active_close:
            print('has close')
            return
        while not self._has_open:
            time.sleep(1)

        self._sub_str = sub_str
        self._ws.send(json.dumps(sub_str))  # as json string to be send
        print(sub_str)

    def close(self):
        self._active_close = True
        self._sub_str = None
        self._has_open = False
        self._ws.close()


if __name__ == '__main__':
    access_key = 'xxx'
    secret_key = 'xxx'

    ################# spot
    print('*****************\nstart spot ws.\n')
    host = 'api.huobi.de.com'
    path = '/ws/v2'
    spot = Ws(host, path, access_key, secret_key, True)
    spot.open()

    # only sub interface
    sub_params = {
        "action": "sub",
        "ch": "accounts.update"
    }
    spot.sub(sub_params)
    time.sleep(10)
    spot.close()
    print('end spot ws.\n')

    ################# future
    print('*****************\nstart future ws.\n')
    host = 'api.hbdm.vn'
    path = '/notification'
    future = Ws(host, path, access_key, secret_key, False)
    future.open()

    # only sub interface
    sub_params = {
        "op": "sub",
        "topic": "accounts.trx"
    }
    future.sub(sub_params)
    time.sleep(10)
    future.close()
    print('end future ws.\n')

    ################# coin-swap
    print('*****************\nstart coin-swap ws.\n')
    host = 'api.hbdm.vn'
    path = '/swap-notification'
    coin_swap = Ws(host, path, access_key, secret_key, False)
    coin_swap.open()

    # only sub interface
    sub_params = {
        "op": "sub",
        "topic": "accounts.TRX-USD"
    }
    coin_swap.sub(sub_params)
    time.sleep(10)
    coin_swap.close()
    print('end coin-swap ws.\n')

    ################# usdt-swap
    print('*****************\nstart usdt-swap ws.\n')
    host = 'api.hbdm.vn'
    path = '/linear-swap-notification'
    usdt_swap = Ws(host, path, access_key, secret_key, False)
    usdt_swap.open()

    # only sub interface
    sub_params = {
        "op": "sub",
        "topic": "accounts_cross.USDT"
    }
    usdt_swap.sub(sub_params)
    time.sleep(10)
    usdt_swap.close()
    print('end usdt-swap ws.\n')
