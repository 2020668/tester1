from django.conf.urls import url
from booktest import views

urlpatterns = [
    url('^index$', views.index, name='index'),
    url('^temp_tags$', views.temp_tags),
    url('^temp_filter$', views.temp_filter),
    url('^temp_inherit$', views.temp_inherit),
    url('^html_escape$', views.html_escape),
    url('^login$', views.login),
    url('^login_check$', views.login_check),
    url('^change_pwd$', views.change_pwd),
    url('^change_pwd_action$', views.change_pwd_action),
    url('^verify_code/$', views.verify_code),
    url('^url_reverse$', views.url_reverse),
    url('^show_args/(\d+)/(\d+)$', views.show_args, name='show_args'),
    url('^show_kwargs/(?P<c>\d+)/(?P<d>\d+)$', views.show_kwargs, name='show_kwargs'),
    url('^test_redirect$', views.test_redirect),
    url('^test_static$', views.test_static),
    url('^show_upload$', views.show_upload),
    url('^upload_handle$', views.upload_handle),
    url('^show_area/page=(?P<pindex>\d*)$', views.show_area),
    url('^areas$', views.areas),
    url('^province$', views.province),
]
