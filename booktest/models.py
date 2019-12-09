from django.db import models


# Create your models here.


class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'bookinfo'


class AreaInfo(models.Model):
    areaCode = models.CharField(max_length=50, verbose_name='地区代码')
    areaName = models.CharField(max_length=20, verbose_name='地区名称')
    level = models.IntegerField()
    cityCode = models.CharField(max_length=50)
    center = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.areaName

    def area_name(self):
        return self.areaName
    area_name.admin_order_field = 'areaName'    # 排序
    area_name.short_description = '地区名称'    # 标题

    def show_parent(self):
        if self.parent is None:
            return ''
        return self.parent.areaName
    show_parent.short_description = '父级地区'


# 上传图片
class PicTest(models.Model):
    goods_pic = models.ImageField(upload_to='booktest')   # 相对与media下的哪个目录

