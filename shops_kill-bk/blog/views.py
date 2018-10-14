from django.shortcuts import render
from django.http import *
from . import models
from django.forms.models import model_to_dict
import time
import datetime
import json
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
import hashlib
from django.db import transaction
from django.http import HttpResponseRedirect

#  商品列表页面
def index(request):
    shops = models.Shops.objects.all()
    for vo in shops:
        vo.percent = int( float(vo.sales) / float(vo.stock) * 100)  # 计算销量百分比，销量/库存

    return render(request, 'blog/index.html', {'shops':shops})

#  商品秒杀页面
def detail(request,sid):
    data = models.Shops.objects.get(id=sid)
    now_time = int(time.time())  #当前时间
    start_time = int(time.mktime(data.starttime.timetuple()))  #datetime转时间戳格式,秒杀开始时间
    end_time = int(time.mktime(data.endtime.timetuple()))  #秒杀结束时间

    return render(request, 'blog/detail.html',{
        'data':data,
        'start_time':json.dumps(start_time), # 传参到js中处理
        'end_time':json.dumps(end_time)
    })


#  注册页面
def regiter(request):
    return render(request, 'blog/regiter.html')


#  登录页面
def login(request):
    return render(request, 'blog/login.html')

#个人中心页面
def person(request):
    uid = request.session.get('uid')
    if not uid:
        return HttpResponseRedirect('/index/login')  #未登录跳转登录页
    list = models.Shop_users.objects.get(id = uid)
    list.addtime = list.addtime.strftime( '%Y-%m-%d' )
    return render(request,'blog/person.html',{'list':list})

#资料修改页面
def data_edit(request):
    uid = request.session.get('uid')  # 用户id
    try:
        Uinfo = models.Shop_users.objects.get( id = uid)
        return render(request, 'blog/data_edit.html',{'Uinfo':Uinfo})
    except:
        return render(request, 'blog/data_edit.html')


#密码修改页面
def password_edit(request):
    return render(request,'blog/password_edit.html')

#订单列表页面
def order_list(request):
    uid = request.session.get('uid')
    if not uid:
        return HttpResponseRedirect('/index/login')  # 检查是否登录,未登录跳转登录页
    print(uid)

    list = models.Orders.objects.filter(uid = uid)  #查询订单表，单签用户下的订单
    if list:
        for x in list:
            shopinfo = models.Shops.objects.filter(id = x.shopid)
            x.img = shopinfo[0].pic
            x.addtime = x.addtime.strftime( '%Y-%m-%d %H:%M:%S' )
    return render(request, 'blog/order_list.html', {'list':list})
    # except:
    #     return render(request, 'blog/order_list.html',{'list':[]})


#积分列表页面
def points_list(request):
    uid = request.session.get('uid')
    score_list = models.Orders.objects.filter(uid = uid)
    Uinfo = models.Shop_users.objects.filter(id = uid)
    Uscore = Uinfo[0].score
    for x in score_list:
        x.addtime = x.addtime.strftime('%Y-%m-%d %H:%M:%S')
    return render(request,'blog/points_list.html',{'score_list':score_list, 'Uscore':Uscore})


#修改地址动作
def edit_data_ajax(request):
    if request.is_ajax():  # 验证是否ajax请求,防止爬虫
        uid = request.session.get('uid')  # 用户id
        phone = request.POST.get('phone')  # 电话
        adress = request.POST.get('adress')  # 地址
        try:
            Uinfo = models.Shop_users.objects.get(id=uid)
            Uinfo.phone = phone
            Uinfo.adress = adress
            Uinfo.save()
            return JsonResponse({'res': '1', 'msg': '修改成功'})
        except:
            return JsonResponse({'res': '-1', 'msg': '啊欧，出错了，请重试'})
    else:
        return JsonResponse({'res': '-1', 'msg': '非法请求'})

#修改密码动作
def edit_pass_ajax(request):
    if request.is_ajax():  #验证是否ajax请求
        uid = request.session.get('uid') #用户id
        password = request.POST.get('password')  # 密码
        oldpassword = request.POST.get('oldpassword')  # 原密码
        print(1222222)
        md5 = hashlib.md5()
        md5_2 = hashlib.md5()
        md5.update(password.encode(encoding='utf-8')) #将原密码进行MD5加密与数据库比对
        password = md5.hexdigest()
        oldpassword = md5_2.update(oldpassword.encode(encoding='utf-8'))
        oldpassword = md5_2.hexdigest()
        print(password)
        print(oldpassword)
        # return
        try:
            Uinfo = models.Shop_users.objects.get(id = uid)
            if Uinfo.password == oldpassword:
                Uinfo.password = password
                Uinfo.save()
                return JsonResponse({'res': '1', 'msg': '修改成功'})
            else:
                return JsonResponse({'res': '-1', 'msg': '原密码错误'})
        except:
            return JsonResponse({'res': '-1', 'msg': '啊欧，出错了，请重试'})
    else:
        return JsonResponse({'res': '-1', 'msg': '非法请求'})


#退出登录动作
def exit_ajax(request):
    if request.is_ajax():  # 验证是否ajax请求
        islogin = request.session.get('isLogin')
        if not islogin:
            return JsonResponse({'res': '-1', 'msg': '尚未登录'})
        else:
            request.session.clear()  # 删除session
            return JsonResponse({'res': '1', 'msg': '退出成功'})
        # except:
        #     return JsonResponse({'res': '-1', 'msg': '操作失败请重试'})
    else:
        return JsonResponse({'res': '-1', 'msg': '非法请求'})

 #  登录验证
def login_ajax(request):
    md5 = hashlib.md5()
    if request.is_ajax():  #验证是否ajax请求
        uname = request.POST.get('uname') #用户名
        password = request.POST.get('password')  # 密码
        md5.update(password.encode(encoding='utf-8'))  # ( 数据库中密码采用md5(sha1()) 加密方法)
        password = md5.hexdigest()
        vcode = request.POST.get('vcode') #提交的验证码
        vcode_session = request.session.get('verifycode') #session中的验证码
        try:
            Uinfo = models.Shop_users.objects.get(name = uname)
        except:
            return JsonResponse({'res': '-1', 'msg': '用户名不存在'})

        #用户名和密码校验
        if password == Uinfo.password and vcode.upper() == vcode_session.upper(): #将验证码同时转为大写比较，即不区分大小写
            # 保存用户的登录状态
            request.session['isLogin'] = True
            request.session['uname'] = uname
            request.session['uid'] = Uinfo.id
            return JsonResponse({'res':'1', 'msg': '登录成功'})
        elif password != Uinfo.password:
            return JsonResponse({'res':'-1', 'msg': '密码错误'})
        elif vcode.upper() != vcode_session.upper():
            return JsonResponse({'res':'-1', 'msg': '验证码错误'})


    else:
        return JsonResponse({'res': '-1', 'msg': '非法请求'})

#   注册动作
def regiter_ajax(request):
    if request.is_ajax():
        uname = request.POST.get('uname')  # 用户名
        password = request.POST.get('password')  # 密码
        adress = request.POST.get('adress')  # 收货地址
        phone = request.POST.get('phone')  # 收货地址
        vcode = request.POST.get('vcode')  # 提交的验证码
        try:
            Uinfo = models.Shop_users.objects.get(name=uname) # 查询数据库用户名是否存在，不存在则抛出异常
            print(Uinfo.score)
            return JsonResponse({'res': '-1', 'msg': '用户名已被注册，换个用户名试试吧'})
        except:
            pass

        vcode_session = request.session.get('verifycode')  # session中的验证码
        if vcode.upper() != vcode_session.upper():  # 将验证码同时转为大写比较，即不区分大小写
            return JsonResponse({'res': '-1', 'msg': '图形验证码错误'})
        if uname.strip() == '' or password.strip() == '' or adress.strip() == '':  # 验证用户名，密码，地址是否为空
            return JsonResponse({'res': '-1', 'msg': '必要参数缺失'})
        # if Uinfo :

        print(password.encode(encoding='utf-8'))
        addtime = datetime.datetime.now()
        md5 = hashlib.md5()
        md5.update(password.encode(encoding='utf-8'))  # 对密码进行MD5加密(前端已进行sha1加密，因此最终密码是双重加密)
        # print(md5)
        password = md5.hexdigest()
        dic = {'name':uname, 'password':password, 'adress':adress, 'addtime':addtime, 'phone':phone}
        # print(dic)
        # return
        try:
            models.Shop_users.objects.create(**dic)
            return JsonResponse({'res': '1', 'msg': '注册成功'})
        except:
            return JsonResponse({'res': '-1', 'msg': '注册失败，请重试'})

    return JsonResponse({'res': '-1', 'msg': '非法请求'})


#  秒杀动作
def kill_ajax(request):
    if request.is_ajax():
        isLogin = request.session.get('isLogin')  # 获取登录信息，判断是否登录
        sid = request.POST.get('sid')  # 商品id

        print(isLogin)
        if not isLogin :
            return JsonResponse({'res': '-2', 'msg': '检测到未登录，是否跳转登录页面'})
        if not sid :
            return JsonResponse({'res': '-1', 'msg': '缺少必要参数'})

        # 启用事务。如果产生了异常，就会回滚这次事务
        shiwu = transaction.savepoint()
        try:
            Uid =  request.session.get('uid')
            print(Uid)
            Shopinfo = models.Shops.objects.get(id = sid)
            Uinfo = models.Shop_users.objects.get(id = Uid)
            start_time = int(time.mktime(Shopinfo.starttime.timetuple()))  # datetime转时间戳格式,秒杀开始时间
            end_time = int(time.mktime(Shopinfo.endtime.timetuple()))  # 秒杀结束时间
            ux_now = time.time()  # 当前时间戳
            m_now = int(ux_now)  # 当前时间戳（秒级，用于转换日期格式）
            hm_now = str(int(ux_now * 1000))[-3:]  # 当前时间戳（毫秒级截取后三位，即当前的毫秒）

            if start_time > ux_now :  # 判断秒杀是否开始
                transaction.savepoint_rollback(shiwu)
                return JsonResponse({'res': '-1', 'msg': '咦？活动还没开始，怎么提交的呢'})
            elif end_time < ux_now:  # 判断秒杀活动是否结束
                transaction.savepoint_rollback(shiwu)
                return JsonResponse({'res': '-1', 'msg': '啊欧，慢了一步，活动已经结束了'})
            elif Shopinfo.stock < 1 :   # 判断库存是否为0
                transaction.savepoint_rollback(shiwu)
                return JsonResponse({'res': '-1', 'msg': '被抢购完了'})
            elif Uinfo.score < Shopinfo.price :  # 判断用户余额是否足够
                transaction.savepoint_rollback(shiwu)
                return JsonResponse({'res': '-1', 'msg': '积分余额不足'})
            else:
                print('kkk')
                Shopinfo.stock -= 1
                Shopinfo.sales += 1
                Shopinfo.save()
                print(Uinfo.score)
                print(Shopinfo.price)
                Uinfo.score = float(Uinfo.score) - float(Shopinfo.price)   #计算用户余额
                Uinfo.save()
                print('ppppp')
                timearray = time.localtime(m_now)
                Uix_now_time = time.strftime("%Y%m%d%H%M%S", timearray)  # 转换日期格式去掉'-'
                ran = random.randint(1000, 9999)   #产生4位随机数
                orderid = '%s%s%s'%(Uix_now_time, hm_now, ran)   # 订单号(拼接字符串,当前日期+下单毫秒+随机数)
                print('lll')
                addtime = datetime.datetime.now()
                dic = {'orderid':orderid, 'shopid':sid, 'uid':Uid, 'shopname':Shopinfo.name,
                       'uname':Uinfo.name, 'adress':Uinfo.adress, 'state':'已支付', 'addtime':addtime, 'paymoney':Shopinfo.price}
                models.Orders.objects.create(**dic)
                transaction.savepoint_commit( shiwu )  # 提交事务的逻辑
                return JsonResponse({'res': '1', 'msg': '秒杀成功！'})
        except:
            #发生异常就回滚
            transaction.savepoint_rollback( shiwu )
            return JsonResponse({'res': '-1', 'msg': '阿欧，出错了，请重试'})
    else:
        return JsonResponse({'res': '-1', 'msg': '非法请求'})



#  图形验证码
def verify_code(request):
    # 定义变量，用于画面的背景色、宽、高
    # 在20到100之间随机找一个数
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 40
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点，防止攻击
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))# 噪点绘制的范围
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))# 噪点的随机颜色
        draw.point(xy, fill=fill) # 绘制出噪点
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'    # 定义验证码的备选值
    rand_str = ''
    for i in range(0, 4):    #随机选取4个值作为验证码
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('arial.ttf', 23)    # 构造字体对象
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))    # 构造字体颜色
    #绘制4个字
    draw.text((5, 6), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 6), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 6), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 6), rand_str[3], font=font, fill=fontcolor)
    del draw     # 释放画笔
    request.session['verifycode'] = rand_str #存入session，用于做进一步验证
    print(rand_str)
    buf = BytesIO()  # 内存文件操作
    im.save(buf, 'png') # 将图片保存在内存中，文件类型为png
    return HttpResponse(buf.getvalue(), 'image/png') # 将内存中的图片数据返回给客户端，MIME类型为图片png






