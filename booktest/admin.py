from django.contrib import admin
from booktest.models import AreaInfo
# Register your models here.


class AreaInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['areaCode', 'areaName', 'parent_id', 'area_name']    # 可写属性和方法


admin.site.register(AreaInfo, AreaInfoAdmin)
