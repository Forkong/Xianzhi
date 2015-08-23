#!/usr/bin/env python
#encoding: utf-8
import string
import random

def mk_md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def warp_data(data):
    data = dict(data)
    for k,v in data.items():
        if isinstance(v, list):
            if len(v)>1:
                data[k] = ','.join(v)
            elif len(v)==1:
                data[k] = v[0]
            else:
                data[k] = ''
        else:
            data[k] = ''
    return data

def now():
    import time
    return time.strftime('%Y-%m-%d %X', time.localtime() )

def handle_uploaded_file(f, suffix):
    try:
        # 生成随机字符串 作为文件名称
        f.name = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'],20)).replace(' ','')
        f.name = f.name+'.'+suffix
        print f.name
        destination = open('static/upload/%s' % f.name,'wb')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        return f.name
    except Exception as e:
        print e
        return False

