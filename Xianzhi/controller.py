from Xianzhi import function as fun
from Xianzhi.models import User, Good

def user_register(pars):
    if pars['passwd']!=pars['repasswd']:
        return -1
    condition = fun.warp_data(pars)
    del condition['repasswd']
    condition['create_date'] = fun.now()
    condition['passwd'] = fun.mk_md5(condition['passwd'])
    print 'condition = ',condition
    try:
        r = User.objects.get(email=condition['email'])
        if r:
            return -2
    except User.DoesNotExist:
        try:
            u = User(**condition)
            u.save()
            if u.name:
                return 1
            else:
                return -3
        except:
            return -2

def user_login(pars):
    email = pars.get('email')
    passwd = fun.mk_md5(pars.get('passwd'))
    condition = {'email':email}
    try:
        r = User.objects.get(**condition)
        if r and r.passwd==passwd:
            return r
    except:
        return None

def user(id):
    try:
        return User.objects.get(id=id)
    except:
        return None

def single_good_info(id):
    try:
        return Good.objects.get(id=id)
    except:
        return {}

def my_good_info(uid):
    try:
        return Good.objects.filter(uid=uid)
    except:
        return {}

def women_good_info():
    try:
        return Good.objects.filter(tag=0)
    except:
        return {}

def men_good_info():
    try:
        return Good.objects.filter(tag=1)
    except:
        return {}

def single_good_save(pars):
    try:
        r = Good.objects.get(id=pars['id'])
        if r:
            r.name = pars['name']
            r.description = pars['description']
            r.phone = pars['phone']
            r.price = pars['price']
            r.tag = pars['tag']
            r.save()
            return 1
        else:
            return -1
    except Exception as e:
        print e
        return -2

def single_good_delete(id):
    try:
        r = Good.objects.get(id=id)
        r.delete()
        return True
    except:
        return False

def single_good_add(pars):
    condition = fun.warp_data(pars)
    condition['create_date'] = fun.now()
    del condition['id']
    print 'condition = ', condition
    try:
        g = Good(**condition)
        g.save()
        return True
    except Exception as e:
        print e
        return False

def single_good_search(name):
    try:
        return Good.objects.filter(name__contains=name)
    except:
        return {}