from django.conf.urls import *
from . import views

app_name = 'market'  #必须要加声明所用的命名空间
urlpatterns=[
    url(r'^$',views.index),
    url(r'^detail/(?P<sid>[0-9]*)$', views.detail, name='detail'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_ajax/$', views.login_ajax, name='login_ajax'),
    url(r'^verify_code/[1-9]*$', views.verify_code, name='verify_code'),
    url(r'^regiter/$', views.regiter, name='regiter'),
    url(r'^regiter_ajax/$', views.regiter_ajax, name='regiter_ajax'),
    url(r'^kill_ajax/$', views.kill_ajax, name='kill_ajax'),
    url(r'^person/$', views.person, name='person'),
    url(r'^data_edit/$', views.data_edit, name='data_edit'),
    url(r'^password_edit/$', views.password_edit, name='password_edit'),
    url(r'^order_list/$', views.order_list, name='order_list'),
    url(r'^points_list/$', views.points_list, name='points_list'),
    url(r'^exit_ajax/$', views.exit_ajax, name='exit_ajax'),
    url(r'^edit_pass_ajax/$', views.edit_pass_ajax, name='edit_pass_ajax'),
    url(r'^edit_data_ajax/$', views.edit_data_ajax, name='edit_data_ajax'),
]