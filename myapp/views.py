from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from myapp.det import detect_and_plot_bounding_box
from myapp.models import *


def adminhome(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    return render(request,"Admin/homeindex.html")

def login(request):
    return render(request,"loginindex.html")

def loginpost(request):
    user=request.POST['textfield']
    pasw=request.POST['textfield2']
    lobj = Login.objects.filter(username=user, password=pasw)
    if lobj.exists():
        log = Login.objects.get(username=user, password=pasw)
        request.session['lid'] = log.id
        if log.type == 'admin':
            return HttpResponse('''<script>alert('logined');window.location='/myapp/adminhome/'</script>''')
        else:
            return HttpResponse('''<script>alert('invalid');window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert('invalid');window.location='/myapp/login/'</script>''')

def Change_password(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    return render(request,"Admin/Change password.html")

def change_password_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    cpass=request.POST['textfield']
    npass=request.POST['textfield2']
    confpass=request.POST['textfield3']
    id = request.session['lid']
    log=Login.objects.get(id=id)
    if log.password==cpass:
        if npass==confpass:
            log.password=npass
            log.save()
            return HttpResponse('''<script>alert('changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('invalid');window.location='/myapp/Change_password/#ab'</script>''')
    else:
        return HttpResponse('''<script>alert('invalid');window.location='/myapp/Change_password/#ab'</script>''')


def view_user(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    data=User.objects.all()
    return render(request,'Admin/View users.html',{'data':data})
def view_user_post (request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    search=request.POST['textfield']
    data = User.objects.filter(name__icontains=search)
    return render(request, 'Admin/View users.html', {'data': data})

def view_c_r(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    data=Complaints.objects.all()
    return render(request,'Admin/view complaint and reply.html',{'data':data})
def view_c_r_post (request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    FromDate = request.POST['textfield']
    ToDate = request.POST['textfield2']
    data = Complaints.objects.filter(date__range=[FromDate,ToDate])
    return render(request, 'Admin/view complaint and reply.html', {'data': data})
def reply_complaint (request,id):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    return render(request, 'Admin/Reply complaint.html', {'id': id})
def reply_complaint_post (request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Please Login');window.location='/myapp/login/'</script>''')
    com = request.POST['textarea']
    id = request.POST['id']
    c=Complaints.objects.get(id=id)
    c.reply=com
    c.status='replied'
    c.save()

    return HttpResponse('''<script>alert('Replied');window.location='/myapp/view_c_r/'</script>''')



def logout(req):
    req.session['lid']=''
    return HttpResponse('''<script>alert('Logout Success');window.location='/myapp/login/#ab'</script>''')



def flutt_signup_post(request):
    photo = request.POST['photo']
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    district = request.POST['district']
    password= request.POST['password']
    cp= request.POST['cp']

    import datetime
    import base64

    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(photo)
    fh = open(r"C:\Users\91815\PycharmProjects\detectinghum\media\\" + date + ".jpg", "wb")
    path = "/media/" + date + ".jpg"
    fh.write(a)
    fh.close()

    if not User.objects.filter(email=email).exists():
        if password==cp:

            log = Login()
            log.username = email
            log.password = password
            log.type = 'user'
            log.save()

            usr = User()
            usr.LOGIN = log
            usr.name = name
            usr.email = email
            usr.gender = gender
            usr.phone = phone
            usr.dob = dob
            usr.postname = post
            usr.place = place
            usr.district = district
            usr.pincode = pin
            usr.photo = path
            usr.save()
            return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"invalid"})
    else:
        return JsonResponse({"status": "no"})

def userlogin(request):
    usr = request.POST['name']
    passw = request.POST['password']
    print(usr)
    print(passw)
    log = Login.objects.filter(username=usr,password=passw)
    if log.exists():
        logg = Login.objects.get(username=usr,password=passw)
        if logg.type == "user":
            ress=User.objects.get(LOGIN_id=logg.id)
            return JsonResponse({"status":"ok",'lid':logg.id,'name':ress.name,'photo':ress.photo,"email":ress.email})
        else:
            return JsonResponse({"status": "not ok"})
    else:
        return JsonResponse({"status":"not ok"})

def view_user_profile(request):
    lid=request.POST['lid']
    usr=User.objects.get(LOGIN_id=lid)
    return JsonResponse({"status":"ok","name":usr.name,"dob":usr.dob,"email":usr.email,"gender":usr.gender,"phone":usr.phone,
                         "place": usr.place, "district": usr.district,"pin": usr.pincode,"photo": usr.photo
                         })

def edit_user_profile(request):
    dname = request.POST['name']
    demail = request.POST['email']
    dgender = request.POST['gender']
    dphone = request.POST['phone']
    ddob = request.POST['dob']
    dplace = request.POST['place']
    ddistrict = request.POST['district']
    dpincode = request.POST['pin']
    image = request.POST['photo']
    lid = request.POST['lid']
    if Login.objects.filter(username=demail).exclude(id=lid).exists():
        return JsonResponse({"status": "no"})

    if len(image)>5:

        import datetime
        import base64

        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        a = base64.b64decode(image)
        fh = open(r"C:\Users\91815\PycharmProjects\detectinghum\media\\" + date + ".jpg", "wb")
        path = "/media/" + date + ".jpg"
        fh.write(a)
        fh.close()
        drv = User.objects.get(LOGIN_id=lid)
        drv.photo = path
        drv.save()
    drv = User.objects.get(LOGIN_id=lid)
    drv.name = dname
    drv.email = demail
    drv.gender = dgender
    drv.phone = dphone
    drv.dob = ddob
    drv.place = dplace
    drv.district = ddistrict
    drv.pincode = dpincode
    drv.save()

    log = Login.objects.get(id=lid)
    log.username = demail
    log.save()
    return JsonResponse({"status":"ok"})
def user_sendcomplaint(request):
    lid=request.POST['lid']
    complaint=request.POST['complaint']
    cobj=Complaints()
    cobj.complaints=complaint
    cobj.reply="pending"
    cobj.status="pending"
    import datetime
    cobj.date=datetime.datetime.now().date()
    cobj.USER=User.objects.get(LOGIN__id=lid)
    cobj.save()
    return JsonResponse({'status': "ok"})


def user_viewreply(request):
    lid=request.POST['lid']
    robj=Complaints.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in robj:
        l.append({'id':i.id,'date':i.date,'complaint':i.complaints,'reply':i.reply,'status':i.status})
    print(l)
    return JsonResponse({'status': "ok",'data':l})


def user_changepassword(request):
    oldpassword=request.POST['oldpassword']
    newpassword=request.POST['newpassword']
    confirmpassword=request.POST['cp']
    lid=request.POST['lid']
    res = Login.objects.filter(id=lid, password=oldpassword)
    if res.exists():
        log = Login.objects.get(id=lid, password=oldpassword)
        if log is not None:
            if newpassword == confirmpassword:
                log = Login.objects.filter(id=lid, password=oldpassword).update(password=confirmpassword)
                return JsonResponse({'status':"ok"})
            else:
                return JsonResponse({'status':"not ok"})
        else:
            return JsonResponse({'status': "not ok"})
    else:
        return JsonResponse({'status': "not ok"})

def user_check(request):
    photo = request.POST['photo']

    import datetime
    import base64

    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(photo)
    fh = open(r"C:\Users\91815\PycharmProjects\detectinghum\media\\" + date + ".jpg", "wb")
    path = "/media/" + date + ".jpg"
    fh.write(a)
    fh.close()

    return JsonResponse({"status": "ok",
                         'img':"/media/det/"+detect_and_plot_bounding_box("C:\\Users\\91815\\PycharmProjects\\detectinghum"+path)[1],
                         'per':detect_and_plot_bounding_box("C:\\Users\\91815\\PycharmProjects\\detectinghum"+path)[0],
                         })