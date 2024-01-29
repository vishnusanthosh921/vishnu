from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from .models import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse,HttpResponse
import random
import re

# Create your views here.
def index(rrr):
    if 'id' in rrr.session:
        se = rrr.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        usr = usersignup.objects.get(id = val)
        cnt = c.count()
        return render(rrr,'index.html',{'cnt':cnt,'usr':usr})
    return render(rrr,'index.html')

def allproducts(r1):
    return render(r1,'allproducts.html')

def categories(r2):
    if 'id' in r2.session:
        se = r2.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        usr = usersignup.objects.get(id = val)
        cnt = c.count()
        return render(r2,'categories.html',{'cnt':cnt,'usr':usr})
    return render(r2,'categories.html')

def about(r3):
    if 'id' in r3.session:
        se = r3.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        usr = usersignup.objects.get(id = val)
        cnt = c.count()
        return render(r3,'about.html',{'cnt':cnt,'usr':usr})
    return render(r3,'about.html')
    
def contactus(r5):
    if 'id' in r5.session:
        se = r5.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        usr = usersignup.objects.get(id = val)
        cnt = c.count()
        return render(r5,'contactus.html',{'cnt':cnt,'usr':usr})
    return render(r5,'contactus.html')
    

def allproducts(a):
    l = products.objects.all()
    return render(a,'allproducts.html',{'l':l})

def loginpage(rr):
    return render(rr,'loginpage.html')



def searchfn(s):
    if 'id' in s.session:
        se = s.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr = val).all()
        cnt = c.count()
        if s.method == 'POST':
            sr = s.POST.get('sr')
            l = products.objects.filter(name__icontains = sr)
            return render(s,'shopitems.html',{'l':l,'cnt':cnt,'usr':usr})
        return render(s,'shopitems.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        if s.method == 'POST':
            sr = s.POST.get('sr')
            l = products.objects.filter(name__icontains = sr)
            return render(s,'shopitems.html',{'l':l})
        return render(s,'shopitems.html',{'l':l}) 
    


def signup(l2):
    if l2.method == 'POST':
        n = l2.POST.get('name')
        e = l2.POST.get('email')
        ph = l2.POST.get('phone')
        u = l2.POST.get('username')
        p = l2.POST.get('password')
        p2 = l2.POST.get('repassword')
        if p == p2:
            if usersignup.objects.filter(username=u).exists():
                messages.info(l2,"Username already exists",extra_tags="signup")
                return redirect(signup) 
            elif usersignup.objects.filter(email=e).exists():
                messages.info(l2,"Email already exists",extra_tags="signup")
                return redirect(signup)  
            else:
                try:
                    y=re.search("(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*?])",p)
                    x=re.findall(r'^[6-9][0-9]{9}',ph)
                    if x==[ph]:
                        if y==None:
                            messages.info(l2,"Password is not strong",extra_tags="signup")
                            return redirect(signup)
                        else:
                            val=usersignup.objects.create(name=n,email=e,phone=ph,username=u,password=p)
                            val.save()  
                            return redirect(login) 
                    else:
                        messages.info(l2,"Not a valid phone number",extra_tags="signup")
                        return redirect(signup)
                except:
                    messages.info(l2,"Invalid input",extra_tags="signup")
        else:
            messages.info(l2,"Password doesn't match",extra_tags="signup")
            return redirect(signup) 

    return render(l2,'loginpage.html')


def login(l1):
    if l1.method=='POST':
        u=l1.POST.get('username')
        p=l1.POST.get('password')
        
        if u=='admin' and p=='12345':
            return render(l1,'myadmin/index.html')
        
        elif usersignup.objects.filter(username=u).exists():
            usr=usersignup.objects.filter(username=u).first()
            if usr.password==p:
                l1.session['id']=[usr.id]
                return render(l1,'index.html',{'usr':usr})
            else:
                messages.info(l1,'Incorrect Password',extra_tags="login")
                return redirect(login)
        else:
            messages.info(l1,'UserName not found',extra_tags="login")
            return redirect(login)
    return render(l1,'loginpage.html')


def logout(l3):
    if 'id' in l3.session:
        l3.session.flush()
        return redirect(index)
    return render(l3,'index.html')


def addcart(r3,wal=0):
    if 'id' in r3.session:
        se = r3.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr = val).all()
        if r3.method == 'POST':
            p = products.objects.filter(id = wal).first()
            usr = usersignup.objects.get(id = val)
            if c:
                f=0
                for i in c:
                    if i.products == p:
                        f=1
                        i.quantity = i.quantity + 1
                        i.save()
                        return redirect(cartt)
                if f==0:
                    val = mycart.objects.create(usr = usr,products = p,quantity = 1,delivered = False)
                    val.save()
                    return redirect(cartt)
            else:
                val = mycart.objects.create(usr = usr,products = p,quantity = 1,delivered = False)
                val.save()
                return redirect(cartt)
    return redirect(login)



def minuscart(d2,de):
    if 'id' in d2.session:
        se = d2.session.get('id')
        val=se[0]
        c=mycart.objects.get(id=de)
        if c.quantity>1:
            c.quantity = c.quantity - 1
            c.save()
        else:
            c.delete()
        return redirect(cartt)
    
def pluscart(d3,de):
    if 'id' in d3.session:
        se = d3.session.get('id')
        val=se[0]
        c=mycart.objects.get(id=de)
        c.quantity = c.quantity + 1
        c.save()
        return redirect(cartt)

    

def deletecart(d1,de):
    if 'id' in d1.session:
        se = d1.session.get('id')
        val = se[0]
        c=mycart.objects.get(id=de)
        c.delete()
    return redirect(cartt)



def single(r22,wal):
    if 'id' in r22.session:
       se = r22.session.get('id')
       val = se[0]
       usr = usersignup.objects.get(id = val)
       c = mycart.objects.filter(usr = wal).all()
       cnt = c.count()
       l = products.objects.filter(id=wal).first()
       return render(r22,'single.html',{'l':l,'cnt':cnt,'usr':usr,'c':c})
    else:
        l=products.objects.filter(id=wal).first()
        return render(r22,'single.html',{'l':l})
    


def laptops(r9):
    if 'id' in r9.session:
        se = r9.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr = val).all()
        cnt = c.count()
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='l':
                l.append(i) 
        return render(r9,'laptops.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='l':
                l.append(i)
        return render(r9,'laptops.html',{'l':l})   


def mobiles(r9):
    if 'id' in r9.session:
        se = r9.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr = val).all()
        cnt = c.count()
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='m':
                l.append(i)
        return render(r9,'laptops.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='m':
                l.append(i)
        return render(r9,'laptops.html',{'l':l})   
        

def cameras(r9):
    if 'id' in r9.session:
        se = r9.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr = val).all()
        cnt = c.count()
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='c':
                l.append(i)
        return render(r9,'laptops.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='c':
                l.append(i)
        return render(r9,'laptops.html',{'l':l})   
        

def headphones(r9):
    if 'id' in r9.session:
        se = r9.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr = val).all()
        cnt = c.count()
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='h':
                l.append(i)
        return render(r9,'laptops.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='h':
                l.append(i)
        return render(r9,'laptops.html',{'l':l})   
        

def powerbanks(r9):
    if 'id' in r9.session:
        se = r9.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr = val).all()
        cnt = c.count()
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='p':
                l.append(i)
        return render(r9,'laptops.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='p':
                l.append(i)
        return render(r9,'laptops.html',{'l':l})   
        

def accessories(r9):
    if 'id' in r9.session:
        se = r9.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr = val).all()
        cnt = c.count()
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='a':
                l.append(i)
        return render(r9,'laptops.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj = products.objects.all()
        l=[]
        for i in obj:
            if i.category=='a':
                l.append(i)
        return render(r9,'laptops.html',{'l':l})   
    
    
    
#admin dashboard
def adminindex(a2):
    return render(a2,'myadmin/index.html')

def adminpro(a2):
    obj = products.objects.all()
    return render(a2,'myadmin/products.html',{'obj':obj})

def bs(a2):
    return render(a2,'myadmin/base.html')


def messagess(a2):
    return render(a2,'myadmin/message.html')


def addproduct(a2):
    if a2.method=='POST':
        n=a2.POST.get('name')
        dc=a2.POST.get('description')
        f=a2.POST.get('features')
        p=a2.POST.get('price')
        d=a2.POST.get('discount')
        c=a2.POST.get('category')
        img=a2.FILES.get('img')
        obj = products.objects.create(name=n,price=p,description=d,features=f,discount=d,category=c,image=img)
        obj.save()
    return render(a2,'myadmin/add-product.html')

def editproduct(a2,wal):
    obj = products.objects.filter(id=wal).first()
    return render(a2,'myadmin/edit-product.html',{'obj':obj})

def editproduct2(a2,wal):
    obj = products.objects.get(id=wal)
    if a2.method=='POST':
        obj.name=a2.POST.get('name')
        obj.description=a2.POST.get('description')
        obj.features=a2.POST.get('features')
        obj.price=a2.POST.get('price')
        obj.discount=a2.POST.get('discount')
        obj.category=a2.POST.get('category')
        obj.image=a2.FILES.get('img')
        obj.save()
        return redirect(adminpro)
    return render(a2,'myadmin/edit-product.html',{'obj':obj})

def deleteproduct(a2,wal):
    obj = products.objects.filter(id=wal).first()
    obj.delete()
    return redirect(adminpro)

def userss(a2):
    obj = usersignup.objects.all()
    return render(a2,'myadmin/users.html',{'obj':obj}) 


def userbooking(a2):
    o = order.objects.all()
    return render(a2,'myadmin/userbooking.html',{'o':o})

def mess1(r):
    l = msg.objects.all()
    return render(r,'myadmin/messages.html',{'l':l})

def reply(r,em):
    l = msg.objects.filter(id=em).first()
    return render(r,'myadmin/replymail.html',{'l':l})

def replymail(r,em):
    if r.method=='POST':
        l=msg.objects.filter(id=em).first()
        n=r.POST.get('message')
        try:
            send_mail('Reply from ELECTRO',f'{n}','settings.EMAIL_HOST_USER',[l.email],fail_silently=False)
            return redirect(mess1)
        except:
            ms = "NETWORK CONNECTION FAILED"
            return render(r, 'myadmin/replymail.html',{'ms':ms})
    return render(r, 'myadmin/replymail.html')


def contact(r5):
    if 'id' in r5.session:
        se = r5.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        if r5.method=='POST':
            n=r5.POST.get('name')
            m=r5.POST.get('mobile')
            e=r5.POST.get('email')
            me=r5.POST.get('message')
            l=msg.objects.create(name=n,mobile=m,email=e,message=me)
            l.save()
            return redirect(contact)
        return render(r5,'contactus.html',{'cnt':cnt,"usr":usr})
    else:
        return redirect(login)



def forgot_password(request):   
    if request.method == 'POST':
        email = request.POST.get('email')
        
        print(email)
        user = usersignup.objects.get(email=email)
        
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user,token=token)

        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        send_mail('Reset your password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
        return render(request,"reset_password.html")
    return render(request,"password_reset_send.html")


def reset_password(request,token):
    password_reset = PasswordReset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    return render(request,"reset_password.html",{'token':token})

def reset_password2(request,token):
    password_reset = PasswordReset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('repeatpassword')
        if repeat_password == new_password:
            password_reset.user.password = new_password
            password_reset.user.save()
            password_reset.delete()
            return redirect(login) 
    return render(request,"reset_password.html")


def cartt(c1):
    if 'id' in c1.session:
        se = c1.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        cl = {}
        t=0
        for i in c:
            cl[i.products]=[i.quantity,i.id,i.products.discount*i.quantity]
            t=t+(i.products.discount*i.quantity)
        usr = usersignup.objects.filter(id=val).first()
        return render(c1,'cart.html',{"usr":usr,"cl":cl,'cnt':cnt,'t':t})
    return redirect(login)




#order section
def placeorder(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)
        if r.method == 'POST':
            if profile.objects.filter(user=usr) == None:
                userprofile = profile()
                userprofile.user = usr
                userprofile.fname = r.POST.get('fname')
                userprofile.lname = r.POST.get('lname')
                userprofile.email = r.POST.get('email')
                userprofile.phone = r.POST.get('phone')
                userprofile.address = r.POST.get('address')
                userprofile.city = r.POST.get('city')
                userprofile.state = r.POST.get('state')
                userprofile.country = r.POST.get('country')
                userprofile.pincode = r.POST.get('pincode')
                userprofile.save()

            neworder = order()
            neworder.user = usr
            neworder.fname = r.POST.get('fname')
            neworder.lname = r.POST.get('lname')
            neworder.email = r.POST.get('email')
            neworder.phone = r.POST.get('phone')
            neworder.address = r.POST.get('address')
            neworder.city = r.POST.get('city')
            neworder.state = r.POST.get('state')
            neworder.country = r.POST.get('country')
            neworder.pincode = r.POST.get('pincode')

            neworder.total_price = t

            neworder.payment_mode = r.POST.get('payment_mode')
            neworder.payment_id = r.POST.get('payment_id')

            trackno = 'Electro'+str(random.randint(1111111,9999999))
            while order.objects.filter(tracking_no=trackno) is None:
                trackno = 'Electro'+str(random.randint(1111111,9999999))
            neworder.tracking_no = trackno
            neworder.save()

            for item in c:
                orderitem.objects.create(
                    orderdet = neworder,
                    product = item.products,
                    price = item.products.discount,
                    quantity = item.quantity
                )

            mycart.objects.filter(usr=val).delete()

            messages.success(r, 'Your order has been placed successfully')

            payMode = r.POST.get('payment_mode')
            if payMode == "Razorpay":
                return JsonResponse({'status':'Your order has been placed successfully'})

        return redirect(index)
    

def razorpaycheck(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)

    return JsonResponse({
        'total_price':t
    })

def orderss(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        o = order.objects.all()
        l=[]
        for i in o:
            if i.user==usr:
                l.append(i)
        return render(r,'myorders.html',{'l':l})
    return render(r,'myorders.html')

def checkout(r4):
    if 'id' in r4.session:
        se = r4.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        cl = {}
        t=0
        for i in c:
            cl[i.products]=[i.quantity,i.id,i.products.discount*i.quantity]
            t=t+(i.products.discount*i.quantity)

        usr = usersignup.objects.filter(id=val).first()
        userprofile = profile.objects.filter(user=usr)

        return render(r4,'checkout.html',{"usr":usr,"cl":cl,'cnt':cnt,'t':t,'userprofile':userprofile})
    else:
        return render(r4,'checkout.html')
    

def profileedit(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        if r.method == 'POST':
            usr.name = r.POST.get('name')
            usr.email = r.POST.get('email')
            usr.phone = r.POST.get('phone')
            usr.save()
            return redirect(index)
        return render(r,'profileedit.html',{'usr':usr})
    return render(r,'profileedit.html')


def adsingle(r6,wal):
    if 'id' in r6.session:
        se = r6.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        l = products.objects.filter(id=wal).first()
        return render(r6,'myadmin/adsingle.html',{'l':l,'cnt':cnt,'usr':usr,'c':c})
    else:
        l = products.objects.filter(id=wal).first()
        return render(r6,'myadmin/adsingle.html',{'l':l})


