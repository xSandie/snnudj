#todo 生成二维码 
import json

import requests


from api.models.WXToken import WXToken



def get_QRCode(signin_order):
    url = 'https://api.weixin.qq.com/wxa/getwxacode?access_token={ACCESS_TOKEN}'

    ACCESS_TOKEN = WXToken.query.get(1).token

    sent_data = {
        'ACCESS_TOKEN': ACCESS_TOKEN
    }
    url_fin = url.format(**sent_data)
    data = {'scene': 'test', 'width': 300,'path':'pages/signIn/signIn',
            'access_token':ACCESS_TOKEN}
    headers = {'Content-Type': 'application/json'}  ## headers中添加上content-type这个参数，指定为json格式
    response = requests.post(url=url_fin, headers=headers, data=json.dumps(data))

    QRCode_Local_url='\\static\\qrcode\\'+str(signin_order.id)+'.jpg'#本地的/static/...的地址
    QRCode_Local_url_to_return='/static/qrcode/'+str(signin_order.id)+'.jpg'
    try:
        from app import OS_PATH
        f = open(OS_PATH+QRCode_Local_url, 'wb')
        f.write(response.content)
        f.close()
        return QRCode_Local_url_to_return
    except Exception as e:
        return False