# -*- coding:utf-8 -*- 
import json

import requests

def wx_decode(code):#微信code解码接口
    code_url='https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'
    APP_id='wx7b78e4de2da56e94'
    from api.config.secure import APP_secret
    sent_data={
        'APPID':APP_id,
        'SECRET':APP_secret,
        'JSCODE':code,
    }
    code_url_fin=code_url.format(**sent_data)
    try:
        s = requests.session()
        rec_raw_data=s.get(code_url_fin)
        rec_json=json.loads(rec_raw_data.text)
        gId=rec_json['openid']#要返回的openId
    except Exception as e:
        gId=None

    return gId
 