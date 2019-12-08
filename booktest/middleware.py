from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class BlockedIPSMiddleware(MiddlewareMixin):
    EXCLUDE_IPS = ['192.168.124.13']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # 视图函数调用之前都会调用
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.EXCLUDE_IPS:
            return HttpResponse('<h1>Forbidden<h1/>')


class TestMiddleware(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        # 服务器启动之后，接受第一个请求的时候调用
        super().__init__(*args, **kwargs)
        print('init')

    def process_request(self, request):
        # 产生request对象之后　进行url配置之前
        print('process_request')
        return HttpResponse('process_request')

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # 调用视图之前被调用，在每个请求上调用，返回None或HttpResponse对象
        print('process_view')

    def process_response(self, request, response):
        # 视图函数调用之后　内容返回浏览器之前
        print('process_response')
        return response


class ExceptionTest1Middleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print('process_exception1')


class ExceptionTest2Middleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print('process_exception2')
