import django_filters
from rest_framework import filters

from student.models import Student


class StuFilter(filters.FilterSet):
    # 自定义过滤的操作
    # name = django_filters.CharFilter(lookup_expr='icontains') -- 指定name字段的过滤条件为icontains

    # 下述表达式如果等号左边的字段为url中的参数名，如果刚好为数据库中的属性，则可直接与数据库中的相应数据进行匹配，如果不是，则
    # 需要在右边括号内的参数中指定对应数据库的哪个属性，并进行匹配，相当于一个映射，匹配成功则返回结果，
    # 否则返回null，其中参数lookup_expr='icontains' -- 为模糊查询，忽略大小写，不写该参数则为精确查找
    s_name = django_filters.CharFilter(lookup_expr='icontains') # 姓名模糊搜索
    tel = django_filters.CharFilter('s_tel') # 电话精确搜索

    status = django_filters.CharFilter('s_status')
    operate_time_min = django_filters.DateTimeFilter('s_operate_time',lookup_expr='gte') # lookup_expr:指定搜索条件
    operate_time_max = django_filters.DateTimeFilter('s_operate_time', lookup_expr='lte')
    chinese_min = django_filters.NumberFilter('s_chinese',lookup_expr='gte')
    chinese_max = django_filters.NumberFilter('s_chinese', lookup_expr='lte')


    class Meta:
        # model -- 该类是为Model Student定义的过滤类
        # fields -- 该过滤类可以处理Student model中字段s_name，s_tel，s_status，s_operate_time,s_chinese的查询
        model=Student
        # 原则上上述过滤涉及的属性在fields应当都有提及，但是由于新版本的缘故，不写也会自动与数据库中
        # 对应的属性匹配，即fields列表中可以为空,但不能没有，为了更好的向下兼容，建议还是写
        fields = ['s_name','s_tel','s_status','s_operate_time','s_chinese']