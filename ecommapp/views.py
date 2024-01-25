from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.

def about(request):

    return render(request,'about.html')

def contact(request):

    return render(request,'contact.html')

def home(request):
 context={}
 p=Product.objects.filter(is_active=True) #filter() method is used to query the database and retrieve a set of objects that match the specified conditions. In this case, you are filtering products based on the is_active field being True.
 print(p)
 context['products']=p
 #userid=request.user.id
 #print("Id of logged in user:",userid)
 #print("Result:",request.user.is_authenticated)
 return render(request,'index.html',context) #render is merging process of database and templates

def product_details(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_details.html',context)
    #return render(request,'product_details.html')

def register(request):
  context={}
  if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']

        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Field cannot empty"
            return render(request,'register.html',context) #first  conditions
        elif upass!=ucpass:                                #second conditions
         context['errmsg']="Password & Confirm Password does't Match"
         return render(request,'register.html',context)
        else:
         try:
          u=User.objects.create(username=uname,email=uname)
          u.set_password(upass)
          u.save()
          context['success']="User created sucessfully please login"
          return render(request,'register.html',context)
         except Exception:
            context['errmsg']="User with same username alreay exists!!"
            return render(request,'register.html',context)
  else:
         return render(request,'register.html')
  
def user_login(request):
      context={}
      if request.method=='POST':
          uname=request.POST['uname']
          upass=request.POST['upass']
          if uname=='' or upass=='':
            context['errmsg']="Fields cannot be empty"
            return render(request,'login.html',context) 
          else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect("/home")
            else:
                context['errmsg']="Invalid Username and Password!!"
                return render(request,'login.html',context)
            #print(u) #its complete username full 
            #print(u.password) #its provide password 
            #print(u.is_superuser) 
         
          
      else:
          return render(request,'login.html')
      
def user_logout(request):     
    logout(request)
    return redirect('/login')

def catfilter(request,cv): #cv is category value fliter products based on cv.
    q1=Q(is_active=True) #Q is a query construction. Q defining is query objects.
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        col='price'  #ascending order
    else:
        col='-price'   #desending order

    p=Product.objects.filter(is_active=True).order_by(col) #If col is 'price', products will be sorted in ascending order; if it's '-price', they will be sorted in descending order.
    context={}
    context['products']=p
    return render(request,'index.html',context) 
    

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__gte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3) #Q is a query construction. Q defining is query objects.
    context={}
    context['products']=p
    #print(min)
    #print(max)
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated: #if user is logged in
      userid=request.user.id
      u=User.objects.filter(id=userid) #database qeiry retrive the set of objects from the database.for specific conditions.
    #print(u[0])
      p=Product.objects.filter(id=pid)
      #check product exist or not
      q1=Q(uid=u[0])                  #Q is a query construction. Q defining is query objects. for userid
      q2=Q(pid=p[0])                    #for productid
      c=Cart.objects.filter(q1 & q2)
      n=len(c)                          #n = len(c): Calculates the number of cart items retrieved. If n is 1, it means the product is already in the cart.
      context={}
      context['products']=p
      if n==1:
        context['msg']="Product already in cart"
      else:
       c=Cart.objects.create(uid=u[0],pid=p[0])
       c.save()
       context['success']="Product added!!"
      return render(request,'product_details.html',context)
    else:
     return redirect('/login')

   
def remove(request,cid):
       c=Cart.objects.filter(id=cid)
       c.delete()
       return redirect('/viewcart')

   
def remove_order(request,oid):
       c=Order.objects.filter(id=oid)
       c.delete()
       return redirect('/placeorder')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    
    if qv=='1': #if qv is 1 =true then its increament by 1
        t=c[0].qty+1 #calculate new quantity
        c.update(qty=t) #update quanatity cart items in database
    else:
         if c[0].qty>1: 
          t=c[0].qty-1   #calculate new quantity
          c.update(qty=t) #update quantity of cart items in database

    return redirect("/viewcart")



def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    print(c)
    s=0
    np=len(c)
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty #s=0+2200=2200|s=2200+600=2800|s=2800+1700=
        
    # Define the discount percentage based on the cart total value
    if s >= 1000:
        discount_percentage = 30  # 10% discount for cart value >= 1000
    else:
        discount_percentage = 15  # 5% discount for cart value < 1000

    # Calculate the discount amount based on the cart total and discount percentage
    discount_amount = (discount_percentage / 100) * s

    # Calculate the discounted total
    discounted_total = s - discount_amount
    if request.session.get('order_placed'):
        del request.session['order_placed']    
    context={}
    context['n']=np
    context['products']=c
    context['total']=s
    return render(request,'cart.html',context)

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print("Order id",oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['n']=np
    return render(request,'placeorder.html',context)

def makepayment(request):
   orders=Order.objects.filter(uid=request.user.id)
   s=0
   np=len(orders)
   for x in orders:
    s=s+x.pid.price*x.qty
    oid=x.order_id

   client = razorpay.Client(auth=("rzp_test_sWX0N9T8sxTQOn", "ykDJtPD3qpdQtdSe2X1EC2oj"))
   data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
   payment = client.order.create(data=data)
   #print(payment)
   context={}
   context['products']=payment
   return render(request,'pay.html',context)

def sendusermail(request):
   uemail=request.user.email
   print(uemail)
   msg="Orders Details are:"
   send_mail(
    "Ekart-order placed sucessfully!!",
    msg,
    "dileshj11@gmail.com",
    [uemail],
    fail_silently=False,
)
   
   return HttpResponse("success")

def edit(request,rid):
    print("Id to be edited:",rid)
    return HttpResponse("It to be edited:"+rid)

def delete(request,rid):
    print("Id to be deleted:",rid)
    return HttpResponse("It to be deleted:"+rid)

class SimpleView(View):

    def get(self,request):
        return HttpResponse("Hello from simple view")
    



    
    