from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
# Create your views here.
from student.models import Student, StudentInfo
from student.serializers import StudentSerializer
from uauth.models import User
from student.filters import StuFilter


def addStu(request):
    if request.method == "GET":
        return render(request,"addstu.html")
    if request.method == "POST":
        # 跳转到学生详情方法中去
        name = request.POST.get("name")
        tel = request.POST.get("tel")
        stu = Student.objects.create(
            s_name=name,
            s_tel=tel
        )
        return HttpResponseRedirect(
            reverse("stu:addinfo",kwargs={'stu_id':stu.id})
        )

import logging
logger = logging.getLogger('stu')  # 选择使用的loggers

from rest_framework import  mixins,viewsets
def index(request):
    if request.method == "GET":

        # 获取所有学生信息
        # ticket = request.COOKIES.get("ticket")
        # if not ticket:
        #     return HttpResponseRedirect('/uauth/login/')
        # if User.objects.filter(u_ticket=ticket).exists():
        #     stuinfos = StudentInfo.objects.all()
        #     return render(request,'index.html',{'stuinfos':stuinfos})
        # else:
        #     return HttpResponseRedirect('/uauth/login/')
        stuinfos = StudentInfo.objects.all()
        logger.info('url: %s method: %s 获取学生信息成功'%(request.path,request.method))
        return render(request, 'index.html', {'stuinfos': stuinfos})

def addStuInfo(request,stu_id):
    if request.method == "GET":
        return render(request,'addstuinfo.html',{"stu_id":stu_id})
    if request.method == "POST":
        s_id = request.POST.get("stu_id")
        s_addr = request.POST.get("addr")
        # 添加头像图片
        img = request.FILES.get('img')
        StudentInfo.objects.create(
            s_addr = s_addr,
            s_id=s_id,
            s_image=img
        )
        return HttpResponseRedirect("/stuapp/index/")

def stuPage(request):
    if request.method == "GET":
        page_id = request.GET.get('page_id',1) # 1:默认页数，str类型
        stus = Student.objects.all()
        paginator = Paginator(stus,3)  #参数1：所有学生信息  参数2：按照每页几条数据分页
        page = paginator.page(int(page_id)) # 获取第page_id页数据
        return render(request, 'index_page.html', {'stus':page})

from rest_framework.response import Response
class StudentEdit(mixins.ListModelMixin,  # 获取所有信息
                  mixins.RetrieveModelMixin, # 获取指定信息，可以通过id来查询
                  mixins.UpdateModelMixin, # 修改指定信息，可以使用put/patch方法
                  mixins.DestroyModelMixin, # 删除指定信息，可以使用delete方法
                  mixins.CreateModelMixin,  # 创建指定信息，可以使用post 方法
                  viewsets.GenericViewSet): # 可以调用get_queryset方法，处理queryset的结果
    # 查询所有信息
    queryset = Student.objects.all()
    # 序列化queryset中的信息
    serializer_class = StudentSerializer
    # 过滤
    filter_class = StuFilter
    def get_queryset(self):
        query = self.queryset
        # 在正式过滤操作前进行预处理，忽略s_delete(软删除标记)为1的元素，并按id降序排列
        return query.filter(s_delete=0).order_by('-id')

    def destroy(self, request, *args, **kwargs):  # 软删除
        instance = self.get_object()
        instance.s_delete = 1
        instance.save()
        return Response({'msg':'删除成功','code':200}) # 返回json数据状态，交给CustomJsonRenderer
                                                         # 的render方法处理

def showStu(request):
    return render(request,"show.html")

def showSpStu(request):
    if request.method == "GET":
        grade = request.GET.get("grade")
        low = request.GET.get("low") # 分数下限
        high = request.GET.get("high")  # 分数上限
        status = request.GET.get("status") # 状态
        start = request.GET.get("start") # 开始时间
        end = request.GET.get("end") # 结束时间
        status_dict = dict(Student.STATUS)
        stus=''
        if low and high and start and end:
            stus = Student.objects.filter(s_chinese__lte=high).filter(s_chinese__gte=low).\
                filter(s_operate_time__lte=end).filter(s_operate_time__gte=start)
        elif grade == 60:
            stus = Student.objects.filter(s_chinese__lt=grade)
        elif low and high:
            stus = Student.objects.filter(s_chinese__lte=high).filter(s_chinese__gte=low)
            # stus = Student.objects.filter(s_chinese__lte=high, s_chinese__gte=low)
        elif status:
            for key,value in status_dict.items():
                if value == status:
                    stus = Student.objects.filter(s_status=key)
        elif start and end:
            stus = Student.objects.filter(s_operate_time__lte=end).filter(s_operate_time__gte=start)

        return render(request,"showSpecificStudents.html",{'stus':stus})