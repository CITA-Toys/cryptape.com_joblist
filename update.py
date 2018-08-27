# -*- coding: utf-8 -*-
# flake8: noqa
import sys
import enum
from qiniu import Auth, put_file, etag
from qiniu import BucketManager
from qiniu import CdnManager
import qiniu.config


class Config(str, enum.Enum):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = os.environ['g_access_key']
    secret_key = os.environ['g_secret_key']
    # 要上传的空间
    bucket_name = os.environ['g_bucket_name']
    # 上传到七牛后保存的文件名
    file = os.environ['g_file']
    # 域名地址
    link = os.environ['g_link']


def update(auth):
    cdn_manager = CdnManager(auth)
    # 需要刷新的文件链接
    urls = [
        '{}/{}'.format(Config.link, Config.file)
    ]
    # 刷新链接
    refresh_url_result = cdn_manager.refresh_urls(urls)
    print(refresh_url_result)


def upload(auth, **kwargs):
    # 生成上传 Token，可以指定过期时间等
    key = Config.file.value
    token = auth.upload_token(Config.bucket_name, key, 3600)

    # 要上传文件的本地路径
    localfile = './jobs.json'
    ret, info = put_file(token, key, localfile)
    print(info)

    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)


# def delete(auth):
#     #初始化BucketManager
#     bucket = BucketManager(auth)

#     #删除bucket_name 中的文件 key
#     ret, info = bucket.delete(Config.bucket_name, Config.file)
#     print(info)
#     assert ret == {}

#     update(auth)


def temp():
    try:
        print('test')
        print(g_link)
    except:
        pass


def main():
    # 构建鉴权对象
    auth = Auth(Config.access_key, Config.secret_key)
    # 上传
    upload(auth)
    # delete(auth)

    # cdn 刷新
    update(auth)


if __name__ == '__main__':
    main()
