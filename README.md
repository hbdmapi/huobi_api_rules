# huobi_api_rules

This is an additional explanation for [Huobi API Doc](https://docs.huobigroup.com/docs/spot/v1/cn)

[![MIT licensed](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE-MIT)
[![Apache-2.0 licensed](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE-APACHE)
<br/><br/>

## What's public
Public means public data, which is not personal data. It's market data.
<br/>Such as kline data, depth data and so on.

### Http public
It means via http `get` methon to get public data.
<br/>All most http get methons are getting public data.
- All the public data are got by http get methon.
- All the params are parts of url when sending request.

### Ws public
It means via websocket to get public data. It can be sub or request.
- When sub private data, you will receive private data for many times.
- When request private data, you will receive private data one time.
- The received data is binary data which was compressed of spot, future, coin-swap, usdt-swap

<br/><br/>

## What's private
Private means private data, which is personal data. It needs your api key to get the data.
<br/>Such as your assets, position and so on.

### Http Private
It means via http `post/get` methon to get private data.
<br/>All http `post` methons are getting private data. 
- In http post interface, the signature params are parts of url. And the other params are parts of body data and they must be json formation.

Some of http `get` methons get private data. 
- In http get interface, all the params are parts of url when sending request.

Signature Illustration:
- The signature methods of the four product(spot, future, coin-swap, usdt-swap) are the same.
- Get the binary data of signature string to make HmacSHA256 string and then the HmacSHA256 string be got base64 string.

The signature string of all as same as follow:
- GET_or_POST<br/>
  lower_case_host_name<br/>
  api_path_starts_with_/<br/>
  AccessKeyId=your_akid&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=url_encode_utc_time


### Ws private
It means via websocket to get private data. It can be sub or request. 
- When sub private data, you will receive private data for many times
- When request private data, you will receive private data one time.
- The received data is binary data which was compressed except spot's account and order pushed messege.
- The pushed messege of spot's account and order are plaintext data.
- In ws private, you must send signature data and then sub/req your request.

Signature Illustration:
- The signature methods of the four product(spot, future, coin-swap, usdt-swap) are the same.
- Get the binary data of signature string to make HmacSHA256 string and then the HmacSHA256 string be got base64 string.

The signature string of spot as same as follow:
- GET<br/>
  lower_case_host_name<br/>
  api_path_starts_with_/<br/>
  accessKey=your_akid&signatureMethod=HmacSHA256&signatureVersion=2.1&timestamp=url_encode_utc_time

The signature string of future, coin-swap, usdt-swap as same as follow:
- GET<br/>
  lower_case_host_name<br/>
  api_path_starts_with_/<br/>
  AccessKeyId=your_akid&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=url_encode_utc_time
<br/><br/>
