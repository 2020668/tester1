from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import F
from django.core.paginator import Paginator
from django.template import loader, RequestContext
from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
from django.urls import reverse
import random
from booktest.models import BookInfo
from booktest.models import PicTest, AreaInfo

# Create your views here.

# EXCLODE_IPS = ['192.168.124.13']


# 装饰器
# def blocked_ip(view_func):
#     def wrapper(request, *view_args, **view_kwargs):
#         user_ip = request.META['REMOTE_ADDR']
#         if user_ip in EXCLODE_IPS:
#             return HttpResponse('<h1>Forbidden<h1/>')
#         else:
#             return view_func(request, *view_args, **view_kwargs)
#     return wrapper


# 登录装饰器
def login_required(view_func):
    # 定义闭包函数
    def wrapper(request, *view_args, **view_kwargs):
        # 判断用户是否登录
        if 'isLogin' in request.session:
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect('/login')

    return wrapper


def my_render(request, template_path, context={}):
    # 加载模板文件　获取一个模板对象
    temp = loader.get_template(template_path)
    # 定义模板上下文　给模板文件传递数据
    context = RequestContext(request, context)
    context.push(locals())
    # 模板渲染　产生一个标准的html内容
    res_html = temp.render(context=locals(), request=request)
    # 返回应答
    return HttpResponse(res_html)


def index(request):
    # return my_render(request, 'booktest/index.html')
    print('调用index')
    num = 'a' + 1
    return render(request, 'booktest/index.html')


def temp_tags(request):
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_tags.html', {'books': books})


def temp_filter(request):
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_filter.html', {'books': books})


def temp_inherit(request):
    return render(request, 'booktest/child.html')


def html_escape(request):
    return render(request, 'booktest/html_escape.html', {'content': '<h1>hello<h1>'})


# 显示登录页面
def login(request):
    # 判断用是否登录
    if 'isLogin' in request.session:
        # 如果用户已登录　则跳转到首页
        return redirect('/change_pwd')
    else:
        # 用户未登录
        # 获取cookie username
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        return render(request, 'booktest/login.html', {'username': username})


# 登录校验视图
def login_check(request):
    # 提交的参数保存在request对象中
    # request.POST保存post提交的参数　QueryDict类型　　
    # 存入数据　q = QueryDict('a=1&b=2&c=3')  取值　q['a']-->1　q.get('a')没有不抛错　q.get('d',5)没有d就返回5
    # 一个key可存多个值　q = QueryDict('a=1&a=2&a=3')  默认取最后一个值,q.getlist('a')返回 ['1','2','3']
    # request.GET保存get提交的参数
    # 获取提交的参数
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')

    # 获取用户输入的验证码
    vcode1 = request.POST.get('vcode')
    # 获取session中的验证码
    vcode2 = request.session.get('verifycode')
    if vcode1 != vcode2:
        return redirect('/login')
    # 进行登录校验,查询数据库
    if username == 'admin' and password == "123456":
        response = redirect('/change_pwd')
        # 判断是否勾选了记住用户名
        if remember == 'on':
            # response.set_cookie('username', username, 'password', password, max_age=7*24*3600)
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
        # 记住用户登录状态　只要session中有isLogin就认为用户已登录
        request.session['isLogin'] = '1'
        request.session['username'] = username
        return response

    else:
        return redirect('/login')


@login_required
def change_pwd(request):
    return render(request, 'booktest/change_pwd.html')


@login_required
def change_pwd_action(request):
    # 获取新密码
    pwd = request.POST.get('pwd')
    username = request.session.get('username')
    # 返回应答
    return HttpResponse('{} 修改密码成功'.format(username))


def verify_code(request):
    # 定义变量，用于画面的背景色、宽、高
    back_ground_color = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), back_ground_color)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 200):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取４个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象 ubuntu的字体路径是/usr/share/fonts/truetype/freefont
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制４个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session 用于进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保持在内存中　格式为png
    im.save(buf, 'png')
    # 将内存中的图片返回给客户端　MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def url_reverse(request):
    return render(request, 'booktest/url_reverse.html')


def show_args(request, a, b):
    return HttpResponse(a + ':' + b)


def show_kwargs(request, c, d):
    return HttpResponse(c + ':' + d)


def test_redirect(request):
    # url = reverse('booktest:index')
    # url = reverse('booktest:show_args', args=(1, 2))
    url = reverse('booktest:show_kwargs', kwargs={'c': 3, 'd': 4})
    return redirect(url)


def test_static(request):
    return render(request, 'booktest/test_static.html')


# 显示上传图片页面
def show_upload(request):
    return render(request, 'booktest/upload_pic.html')


# 上传图片处理
def upload_handle(request):
    # 获取上传文件的处理对象
    pic = request.FILES['pic']      # pic.name 可获取图片的名字　pic_chunks()返回一个生成器　每次返回一块内容　可遍历读取
    print(type(pic))
    # 创建一个文件
    save_path = '%s/booktest/%s' % (settings.MEDIA_ROOT, pic.name)
    with open(save_path, 'wb') as f:
        # 获取上传文件的内容病写到创建的文件中
        for content in pic.chunks():
            f.write(content)
    # 向数据库中保持上传记录
    PicTest.objects.create(goods_pic='booktest/%s' % pic.name)

    # 返回
    return HttpResponse('ok')


# 前端访问需传递页码
def show_area(request, pindex):
    # 查询出所有省级地区的信息
    areas = AreaInfo.objects.filter(id=F('parent_id'))
    # 分页 每页显示１０条数据
    paginator = Paginator(areas, 10)
    # 获取第１页的对象 page是Page类的实例对象
    # 获取pindex页的内容
    if pindex == '':
        pindex = 1
    else:
        pindex = int(pindex)
    page = paginator.page(pindex)

    # 使用模板
    return render(request, 'booktest/show_area.html', {'page': page})


def areas(request):
    return render(request, 'booktest/areas.html')


# 获取所有省级的地区
def province(request):
    # 查询出所有省级地区的信息
    areas = AreaInfo.objects.filter(id=F('parent_id'))
    # 遍历areas 拼接出json数据　地区名称　id areaName
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.areaName))
    # 返回数据
    return JsonResponse({'data': areas_list})


def city(request, pid):
    # 获取pid下级地区的信息
    # area = AreaInfo.objects.get(id=pid)
    # areas = area.areainfo_set.all()
    areas = AreaInfo.objects.filter(parent_id=pid)
    # 遍历areas 拼接出json数据　地区名称　id areaName
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.areaName))
    # 返回数据
    return JsonResponse({'data': areas_list})


