from flask import Blueprint, request, url_for
from models import Image, Runtime, User
import settings
import requests
import hashlib
import xmltodict
import time
import shortuuid

appid = settings.wc_appid
secret = settings.wc_secret
wc_id = settings.wc_id
wc_token = settings.wc_token

wc = Blueprint('wc', __name__, template_folder='templates', url_prefix='/wc/')
system_user, _ = User.objects.get_or_create(username='SYSTEM', email='1@1.com', active=False)

try:  # may be replaced by get_or_create()
    runtime = Runtime.objects.get(rid=0)
except:
    runtime = Runtime(rid=0).save()


def update_access_token():
    d = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            appid, secret
        )
    ).json()
    if not d.get('errcode'):
        runtime.wc_access_token = d['access_token']
        runtime.wc_access_token_time = int(time.time())
        runtime.save()


def current_access_token():
    if int(time.time()) - runtime.wc_access_token_time >= 7000:
        update_access_token()
    return runtime.wc_access_token




@wc.route('/', methods=['get'])
def main():
    signature = request.args.get('signature', 's')
    string = request.args.get('echostr', 'e')
    timestamp = request.args.get('timestamp', 't')
    nonce = request.args.get('nonce', 'n')
    token = wc_token
    temp_string = ''.join(sorted([token, timestamp, nonce]))
    hash_object = hashlib.sha1(temp_string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    if hex_dig == signature:
        return string
    else:
        return ''


def xml_response(data):
    d = {'xml': data}
    return xmltodict.unparse(d)


def send_text(to, msg):
    res = dict()
    res['ToUserName'] = to
    res['FromUserName'] = wc_id
    res['CreateTime'] = int(time.time())
    res['MsgType'] = 'text'
    res['Content'] = msg
    return xml_response(res)


@wc.route('/', methods=['post'])
def receive():
    data = request.data
    data = xmltodict.parse(data)['xml']
    if data['MsgType'] == 'text':
        return send_text(data['FromUserName'], 'hi')
    if data['MsgType'] == 'image':
        token = current_access_token()
        file_url = 'https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (token, data['MediaId'])
        file = requests.get(file_url, stream=True).raw
        i = Image()
        i.image = file
        uuid = shortuuid.ShortUUID().random(length=6)
        while Image.objects(iid=uuid):
            uuid = shortuuid.ShortUUID().random(length=6)
        i.iid = uuid
        i.title = data['MediaId']
        i.user = system_user
        i.description = ''
        i.tags = []
        i.save()
        return send_text(
            data['FromUserName'], '上传成功！图片地址：%s%s' % (
                request.url_root[:-1], url_for('light-cms.image', iid=i.iid)
            )
        )
