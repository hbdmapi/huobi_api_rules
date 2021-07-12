import websocket
import threading
import time
import json
import gzip


class Ws:
    def __init__(self, host: str, path: str):
        self._host = host
        self._path = path
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
        self._has_open = True

    def _on_msg(self, ws, message):
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

    def req(self, req_str: dict):
        if self._active_close:
            print('has close')
            return
        while not self._has_open:
            time.sleep(1)

        self._ws.send(json.dumps(req_str))  # as json string to be send
        print(req_str)

    def close(self):
        self._active_close = True
        self._sub_str = None
        self._has_open = False
        self._ws.close()


if __name__ == '__main__':
    ################# spot
    print('*****************\nstart spot ws.\n')
    host = 'api.huobi.de.com'
    path = '/ws'
    spot = Ws(host, path)
    spot.open()

    # only sub interface
    sub_params = {'sub': 'market.btcusdt.kline.1min'}
    spot.sub(sub_params)
    time.sleep(10)
    spot.close()
    print('end spot ws.\n')

    ################# future
    print('*****************\nstart future ws.\n')
    host = 'api.hbdm.vn'
    path = '/ws'
    future = Ws(host, path)
    future.open()

    #req
    req_params = {
        "req": "market.BTC_CQ.kline.1min",
        "from": 1626056541,
        "to": 1626057541
    }
    future.req(req_params)
    time.sleep(10)

    #sub
    sub_params = {'sub': 'market.BTC_CQ.kline.1min'}
    future.sub(sub_params)
    time.sleep(10)
    future.close()
    print('end future ws.\n')

    ################# coin-swap
    print('*****************\nstart coin-swap ws.\n')
    host = 'api.hbdm.vn'
    path = '/swap-ws'
    coin_swap = Ws(host, path)
    coin_swap.open()

    #req
    req_params = {
        "req": "market.BTC-USD.kline.1min",
        "from": 1626056541,
        "to": 1626057541
    }
    coin_swap.req(req_params)
    time.sleep(10)

    #sub
    sub_params = {'sub': 'market.BTC-USD.kline.1min'}
    coin_swap.sub(sub_params)
    time.sleep(10)
    coin_swap.close()
    print('end coin-swap ws.\n')

    ################# usdt-swap
    print('*****************\nstart usdt-swap ws.\n')
    host = 'api.hbdm.vn'
    path = '/linear-swap-ws'
    usdt_swap = Ws(host, path)
    usdt_swap.open()

    #req
    req_params = {
        "req": "market.BTC-USDT.kline.1min",
        "from": 1626056541,
        "to": 1626057541
    }
    usdt_swap.req(req_params)
    time.sleep(10)

    #sub
    sub_params = {'sub': 'market.BTC-USDT.kline.1min'}
    usdt_swap.sub(sub_params)
    time.sleep(10)
    usdt_swap.close()
    print('end usdt-swap ws.\n')
