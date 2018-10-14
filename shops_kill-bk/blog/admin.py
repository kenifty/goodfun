from django.contrib import admin, messages
from .models import Shops
from .models import Shop_users
from .models import Orders
from django import forms


class ShopsAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ( 'name', 'price', 'stock', 'sales', 'addtime')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 10
    # ordering设置默认排序字段，负号表示降序排序
    #ordering = ('-id',)
    # list_editable 设置默认可编辑字段
    #list_editable = ['name', 'price']
    # fk_fields 设置显示外键字段
    #fk_fields = ('stock',)
    list_filter = ('addtime',) #筛选字段
    search_fields = ('name', 'price',)  # 搜索字段

class Shop_usersAdmin(admin.ModelAdmin):
    list_display = ('name','score','adress','addtime')
    list_per_page = 10
    search_fields = ('name', )  # 搜索字段
    list_filter = ('addtime',)  # 筛选字段


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'shopname', 'uname', 'state', 'paymoney', 'adress', 'addtime')
    list_per_page = 10
    search_fields = ('orderid', 'shopname', 'uname',)  # 搜索字段
    list_filter = ('addtime','state')  # 筛选字段

admin.site.site_header = '商品管理系统'  # 此处设置页面显示标题
admin.site.site_title = '商品管理系统'  # 此处设置页面头部标题
admin.site.register(Shops,ShopsAdmin,)
admin.site.register(Shop_users,Shop_usersAdmin,)
admin.site.register(Orders, OrdersAdmin,)

