# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag
from qiniu import BucketManager
from qiniu import CdnManager
import qiniu.config
from config import Config


# def delete(auth):
#     from qiniu import Auth
#     from qiniu import BucketManager
#     access_key = 'Access_Key'
#     secret_key = 'Secret_Key'
#     #初始化Auth状态
#     q = Auth(access_key, secret_key)
#     #初始化BucketManager
#     bucket = BucketManager(q)
#     #你要测试的空间， 并且这个key在你空间中存在
#     bucket_name = 'Bucket_Name'
#     key = 'python-logo.png'
#     #删除bucket_name 中的文件 key
#     ret, info = bucket.delete(bucket_name, key)
#     print(info)
#     assert ret == {}



def update(auth):
    print('刷新')
    cdn_manager = CdnManager(auth)
    # 需要刷新的文件链接
    urls = [
        '{}/{}'.format(Config.link, Config.file)
    ]
    # 刷新链接
    refresh_url_result = cdn_manager.refresh_urls(urls)
    print(refresh_url_result)


def upload(auth, **kwargs):
    print('上传')
    # 生成上传 Token，可以指定过期时间等
    key = Config.file.value
    token = auth.upload_token(Config.bucket_name, key, 60)

    # 要上传文件的本地路径
    localfile = './jobs.json'
    ret, info = put_file(token, key, localfile)
    print(info)

    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

    update(auth)


def delete(auth):
    print('删除')
    #初始化BucketManager
    bucket = BucketManager(auth)

    #删除bucket_name 中的文件 key
    ret, info = bucket.delete(Config.bucket_name, Config.file)
    print(info)
    assert ret == {}

    update(auth)


def temp():
    try:
        print('test')
        print(g_link)
    except:
        pass


def main():
    # 构建鉴权对象
    auth = Auth(Config.access_key, Config.secret_key)
    #删除
    # delete(auth)
    # 上传
    upload(auth)

    # cdn 刷新
    # update(auth)


if __name__ == '__main__':
    main()
