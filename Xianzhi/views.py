#encoding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import controller
import function as fun
import time

def index(req):
    return render_to_response('index.html', locals(), context_instance = RequestContext(req))

def login(req):
    if req.method == 'GET':
        return render_to_response('login.html', locals(), context_instance = RequestContext(req))

    data = fun.warp_data(req.POST)
    rt = controller.user_login(data)
    if rt:
        req.session['islogin'] = True
        user_info = {}
        user_info['id'] = rt.id
        user_info['name'] = rt.name
        user_info['email'] = rt.email
        req.session['user_info'] = user_info
        return HttpResponseRedirect('/')
    else:
        msg = '用户名或密码错误，登录失败！'
        return render_to_response('login.html', locals(), context_instance = RequestContext(req))

def register(req):
    if req.method == 'GET':
        return render_to_response('register.html', locals(), context_instance = RequestContext(req))
    else:
        data = req.POST
        print data
        rt = controller.user_register(data)
        if rt>=1:
            msg = '恭喜注册完成，请直接登录！'
            return HttpResponseRedirect('login')
        elif rt==-1:
            msg = '密码设置不一致，请重新设置！'
            return render_to_response('register.html', locals(), context_instance = RequestContext(req))
        elif rt==-2:
            msg = '此邮箱已注册，请直接登录!'
            return render_to_response('register.html', locals(), context_instance = RequestContext(req))
        else:
            msg = '注册失败，请联系管理员!'
            return render_to_response('register.html', locals(), context_instance = RequestContext(req))

def logout(req):
    req.session['islogin'] = False
    req.session['user_info'] = {}
    return HttpResponseRedirect('/')

def mygoods(req):
    if not req.session.get('islogin'):
        msg = '你当前还没有登录，请先登录！'
        return render_to_response('mygoods.html', locals())

    uid = req.session['user_info']['id']
    goods_info = controller.my_good_info(uid)
    return render_to_response('mygoods.html', locals(), context_instance = RequestContext(req))

def women(req):
    goods_info = controller.women_good_info()
    return render_to_response('women.html', locals(), context_instance = RequestContext(req))

def men(req):
    goods_info = controller.men_good_info()
    return render_to_response('men.html', locals(), context_instance = RequestContext(req))

def single(req):
    data = req.GET
    if data['id']:
        is_can_config = False
        single_info = controller.single_good_info(data['id'])
        if req.session.get('islogin'):
            uid = req.session['user_info']['id']
            if uid == single_info.uid.id:
                is_can_config = True
        return render_to_response('single.html', locals(), context_instance = RequestContext(req))
    else:
        msg = '查无此商品，请联系管理员'
        return render_to_response('single.html', locals(), context_instance = RequestContext(req))

def singleadd(req):
    if not req.session.get('islogin'):
        msg = '你当前还没有登录，请先登录！'
        return render_to_response('singleadd.html', locals(), context_instance=RequestContext(req))

    if req.method=='GET':
        return render_to_response('singleadd.html', locals(), context_instance=RequestContext(req))
    else:
        data = req.POST
        uid = req.session['user_info']['id']
        data['uid'] = controller.user(uid)

        f = req.FILES.get('photo', None)
        if not f:
            msg= '您必须给您的商品添加图片'
            return render_to_response('singleadd.html', locals(), context_instance=RequestContext(req))

        name_array = str(f.name).split('.')
        if len(name_array) < 2:
            msg = '图片上传格式不正确，只能为jpg png jpeg格式'
            return render_to_response('singleadd.html', locals(), context_instance=RequestContext(req))
        else:
            if name_array[-1] == 'jpg' or name_array[-1] == 'png' or name_array[-1] == 'jpeg' or name_array[-1] == 'PNG' or name_array[-1] == 'JPG' or name_array[-1] == 'JPEG':
                name = fun.handle_uploaded_file(f, name_array[-1])
                if name == False:
                    msg = '图片上传失败，请稍后重试'
                    return render_to_response('singleadd.html', locals(), context_instance=RequestContext(req))
                else:
                    #上传成功
                    data['photo_name'] = name
                    data['photo_path'] = '/static/upload/'+name
                    if controller.single_good_add(data):
                        return HttpResponseRedirect('mygoods')
                    else:
                        msg = '添加商品失败，请稍后重试'
                        return render_to_response('singleadd.html', locals(), context_instance=RequestContext(req))
            else:
                msg = '图片上传格式不正确，只能为jpg png jpeg格式'
                return render_to_response('singleadd.html', locals(), context_instance=RequestContext(req))

def singleconfig(req):
    if not req.session.get('islogin'):
        msg = '你当前还没有登录，请先登录！'
        return render_to_response('singleconfig.html', locals(), context_instance=RequestContext(req))

    if req.method=='GET':
        data = req.GET
        uid = req.session['user_info']['id']
        single_info = controller.single_good_info(data['id'])
        if uid == single_info.uid.id:
            return render_to_response('singleconfig.html', locals(), context_instance=RequestContext(req))
        else:
            msg = '您没有权限修改此商品!!!'
            return render_to_response('singleconfig.html', locals(), context_instance=RequestContext(req))
    else:
        data = req.POST
        print data
        result = controller.single_good_save(data)
        if result == 1:
            #成功
            return HttpResponseRedirect('single?id='+data['id'])
        elif result == -1:
            msg = '编辑失败，此商品已失效或过期!!!'
            return render_to_response('singleconfig.html', locals(), context_instance=RequestContext(req))
        else:
            msg = '编辑失败，请联系管理员!!!'
            return render_to_response('singleconfig.html', locals(), context_instance=RequestContext(req))

def single_config(req):
    if req.method=='POST':
        data = req.POST
        return HttpResponseRedirect('singleconfig?id='+data['id'])

def singledelete(req):
    if req.method=='POST':
        data = req.POST
        if controller.single_good_delete(data['id']):
            # 删除成功
            return HttpResponseRedirect('mygoods')
        else:
            # 删除失败
            is_can_config = False
            single_info = controller.single_good_info(data['id'])
            msg = '删除失败，请联系管理员'
            if req.session.get('islogin'):
                uid = req.session['user_info']['id']
                if uid == single_info.uid.id:
                    is_can_config = True
            return render_to_response('single.html', locals(), context_instance = RequestContext(req))

def singlesearch(req):
    if req.method == 'POST':
        data = req.POST
        goods_info = controller.single_good_search(data['search_name'])
        return render_to_response('singlesearch.html', locals(), context_instance = RequestContext(req))

