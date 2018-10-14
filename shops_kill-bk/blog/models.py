from django.db import models
from DjangoUeditor.models import UEditorField
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin, messages
import hashlib
#from DjangoUeditor.widgets import UEditorWidget
#from DjangoUeditor.forms import  UEditorField,UEditorModelForm
#import django.utils.timezone as timezone

class Shops(models.Model):
    name = models.CharField(max_length=255,null=True, verbose_name="名称" )
    price = models.DecimalField(null=True, max_digits=16, decimal_places=2, verbose_name="价格")
    oldprice = models.DecimalField(null=True, max_digits=16, decimal_places=2, verbose_name='原价')
    stock = models.IntegerField(null=True, verbose_name="库存")
    sales = models.IntegerField(null=True, verbose_name='销量')
    pic = models.ImageField(upload_to='img', null=True, verbose_name="形象图")
    starttime = models.DateTimeField(editable=True, verbose_name="抢购开始时间", null=True)
    endtime = models.DateTimeField(editable=True, verbose_name="抢购结束时间", null=True)
    # 使发布时间显示在列中
    addtime = models.DateTimeField(editable=True, auto_now_add=True, verbose_name="发布时间", null=True)
    text = UEditorField('详情',width=600, height=300, toolbars="full", imagePath="upload/ueditor/img/", filePath="upload/ueditor/img/", upload_settings={"imageMaxSize":1204000},
             settings={},command=None,event_handler='',blank=True,null=True)

    class Meta:   #中文表名
        verbose_name = '商品列表'
        # 末尾不加s
        verbose_name_plural = '商品列表'
    def __str__(self):
      return self.name


class Shop_users(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="用户名")
    password = models.CharField(max_length=255, null=True, verbose_name="密码", editable=False)  # 后台不可修改
    score = models.FloatField(default=5000, verbose_name='用户积分')   # 初始积分5000
    phone = models.CharField(max_length=255, null=True, verbose_name='联系电话')
    adress = models.CharField(max_length=255, null=True, verbose_name='收货地址')
    #readonly_fields = ('image_data',)  # 必须加这行 否则访问编辑页面会报错
    addtime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间",null=True,editable=True)

    class Meta:   #中文表名
        verbose_name = '商城用户'
        # 末尾不加s
        verbose_name_plural = '商城用户'

    # def save(self, force_insert=False, force_update=False, using=None,   #定制save事件，商城用户不可通过后台新增修改
    #          update_fields=None):
    #     return

    def __str__(self):
        return self.name


#  订单表
class Orders(models.Model):
    orderid = models.CharField(max_length=50, null=False, verbose_name="订单号")
    shopid = models.IntegerField(null=False, verbose_name="商品id", editable=False)
    uid = models.IntegerField(null=False, verbose_name="用户id", editable=False)  # 后台不可修改
    shopname = models.CharField(max_length=255, null=True, verbose_name='商品名称')
    uname = models.CharField(max_length=255, null=True, verbose_name='用户名')
    adress = models.CharField(max_length=255, null=True, verbose_name='收货地址')
    state = models.CharField(max_length=255, null=True, verbose_name='订单状态')  # 未支付，已支付，已发货
    # readonly_fields = ('image_data',)  # 必须加这行 否则访问编辑页面会报错
    addtime = models.DateTimeField(verbose_name="订单生成时间", null=False)
    paymoney = models.DecimalField(null=True, max_digits=16, decimal_places=2, verbose_name='支付价格')
    class Meta:  # 中文表名
        verbose_name = '订单列表'
        # 末尾不加s
        verbose_name_plural = '订单列表'

    # def save(self, force_insert=False, force_update=False, using=None,  # 定制save事件，订单不可通过后台新增修改
    #          update_fields=None):
    #     return

    def __str__(self):
        return self.orderid