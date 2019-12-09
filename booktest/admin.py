from django.contrib import admin
from booktest.models import AreaInfo, PicTest


# Register your models here.


class AreaStackedInline(admin.StackedInline):
    # 写多类的名字
    model = AreaInfo    # 关联子对象
    extra = 2   # 额外关联２个子对象


class AreaTabularInline(admin.TabularInline):
    # 写多类的名字
    model = AreaInfo    # 关联子对象
    extra = 2   # 额外关联２个子对象


class AreaInfoAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示１０条记录
    list_display = ['areaCode', 'areaName', 'parent_id', 'area_name', 'show_parent']  # 可写属性和方法
    actions_on_bottom = True    # 显示地２个下来列表框
    actions_on_top = False  # 关闭顶部的下拉列表框
    list_filter = ['areaName']  # 列表页右侧过滤栏
    search_fields = ['areaCode', 'areaName']    # 搜索框

    # fields = ['parent', 'areaName']     # 标题跟parent对调上下顺序
    fieldsets = (
        ('基本', {'fields': ['areaName']}),
        ('高级', {'fields': ['parent']})
    )

    # inlines = [AreaStackedInline]
    inlines = [AreaTabularInline]


admin.site.register(AreaInfo, AreaInfoAdmin)    # 注册模型类

admin.site.register(PicTest)



