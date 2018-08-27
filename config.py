
import os
import enum


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
