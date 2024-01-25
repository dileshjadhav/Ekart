
from django.urls import path
from ecommapp import views
from ecommapp.views import SimpleView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('about',views.about),
    path('contact',views.contact),
    path('home',views.home),
    path('edit/<rid>',views.edit),
    path('delete/<rid>',views.delete),
    path('myview',SimpleView.as_view()),
    path('pdetails/<pid>',views.product_details),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendusermail),
    path('remove_order/<oid>',views.remove_order),
]

if settings.DEBUG:
   urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)