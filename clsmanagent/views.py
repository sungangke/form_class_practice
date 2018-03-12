from django.shortcuts import render,redirect,HttpResponse
from django.forms import Form, fields,widgets
from clsmanagent import models


# 班级form验证
class ClassForm(Form):
    title = fields.RegexField('全栈\d+',label='班级名称')


# 班级信息
def class_list(request):
    # if request.method == "GET":
    obj = models.Classes.objects.all()
    return render(request, 'classlist.html', {'obj': obj})

#添加班级
def add_class(request):
    if request.method == "GET":
        obj = ClassForm()
        return render(request,'addclass.html',{'obj':obj})
    else:
        obj = ClassForm(request.POST)
        if obj.is_valid():
            models.Classes.objects.create(**obj.cleaned_data)
            return redirect('/class_list/')
        return render(request, 'addclass.html', {'obj': obj})

#编辑班级信息
def edit_class(request,nid):
    if request.method == "GET":
        cls_info = models.Classes.objects.filter(id=nid).first()
        print(cls_info)
        obj = ClassForm(initial={'title':cls_info.title})
        return render(request,'editclass.html',{'obj':obj,'nid':nid})
    else:
        obj = ClassForm(request.POST)
        if obj.is_valid():
            models.Classes.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/class_list/')
        return render(request,'editclass.html',{'obj':obj,'nid':nid})

#学生列表
def student_list(request):
    stu_list = models.Student.objects.all()
    return render(request,'studentlist.html',{'stu_list':stu_list})

#添加学生
##创建学生的Form条件验证
class StuForm(Form):
    sname = fields.CharField(min_length=2,max_length=6,label='学生姓名')
    email = fields.EmailField()
    age = fields.IntegerField()
    cls_id = fields.IntegerField(
        widget=widgets.Select(choices=models.Classes.objects.values_list('id','title'))
    )
def add_stu(request):
    if request.method == "GET":
        obj = StuForm()
        return render(request,'addstudent.html',{'obj':obj})
    else:
        obj = StuForm(request.POST)
        if obj.is_valid():
            models.Student.objects.create(**obj.cleaned_data)
            return redirect('/student_list/')
        return render(request,'addstudent.html',{'obj':obj})

#编辑学生
def edit_stu(request,nid):
    if request.method == "GET":
        row = models.Student.objects.filter(id=nid).values('sname','email','age','cls_id').first()
        obj = StuForm(row)
        return render(request,'editstudent.html',{'obj':obj,'nid':nid})
    else:
        obj = StuForm(request.POST)
        if obj.is_valid():
            models.Student.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/student_list/')
        return render(request,'editstudent.html',{'obj':obj,'nid':nid})


#老师列表
# class TeachForm(Form):
#     tname = fields.CharField(min_length=2)
#     c2t = fields.MultipleChoiceField(
#         choices=models.Classes.objects.values_list('title').all()
#         widget=widgets.Select()
#     )

def teacher_list(request):
    if request.method == "GET":
        teach_list = models.Teacher.objects.all()
        return render(request,'teacher.html',{'teach_list':teach_list})

class TeachForm(Form):
    tname = fields.CharField(min_length=2)
    xx = fields.MultipleChoiceField(
        choices=models.Classes.objects.values_list('id', 'title'),
        widget=widgets.SelectMultiple()
    )

    def __init__(self,*args,**kwargs):
        super(TeachForm,self).__init__(*args,**kwargs)
        self.fields['xx'].widget.choices = models.Classes.objects.values_list('id','title')
    #上面这个显示的结果是可以多选，但是clean_data的数据都是字符串格式，对于取值是很麻烦的

    # xx = fields.CharField(
    #     widget=widgets.Select(choices=models.Classes.objects.values_list('id','title'))
    # )#这样显示出来的是一个单选的下拉框格式

def add_teacher(request):
    if request.method == "GET":
        obj = TeachForm()
        return render(request,'addteacher.html',{'obj':obj})
    else:
        obj = TeachForm(request.POST)
        if obj.is_valid():
            # models.Teacher.objects.create(tname=obj.cleaned_data['tname'])第一种方法，但是对于字段多来说不好用
            niubi = obj.cleaned_data.pop('xx')
            row = models.Teacher.objects.create(**obj.cleaned_data)
            print(type(row))
            row.c2t.add(*niubi)
            return redirect('/teacher/')
        return render(request,'addteacher.html',{'obj':obj})

def edit_teacher(request,nid):
    if request.method == "GET":
        row = models.Teacher.objects.filter(id = nid).first()
        class_id = row.c2t.values_list('id')
        id_list = list(zip(*class_id))[0] if list(zip(*class_id)) else []
        obj = TeachForm(initial={'tname':row.tname,'xx':id_list})

        return render(request,'editteacher.html',{'obj':obj,'nid':nid})
    else:
        obj=TeachForm(request.POST)
        if obj.is_valid():
            #print(obj.cleaned_data)
            yy = obj.cleaned_data.pop('xx')
            print(obj.cleaned_data)
            models.Teacher.objects.filter(id=nid).update(**obj.cleaned_data)
            row = models.Teacher.objects.filter(id=nid).first()
            print(type(row))
            row.c2t.add(*yy)

            return redirect('/teacher/')
        return render(request,'editteacher.html',{'obj':obj})

