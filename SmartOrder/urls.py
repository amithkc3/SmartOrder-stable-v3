"""SmartOrder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from customer import views
from django.contrib.auth import views as auth_views
from . import views as Rviews
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.loginpage,name="loginpage"),
    path('menu/<str:tokenNum>/<str:category>',views.menu,name="menu"),
    path('menuConfirmation/<str:tokenNum>',views.menuConfirmation,name="menuConfirmation"),
    path('ack/',views.ack,name="ack"),
    path('placeOrder/',views.placeOrder,name="placeOrder"),
    
    url('managerLogin/',auth_views.LoginView.as_view(template_name='managerLogin.html'),name="managerLogin"),
    url('managerLogout/',auth_views.LogoutView.as_view(template_name='managerLogout.html'), name="managerLogout"),
    

    path('currentOrders/',Rviews.currentOrderList,name="currentOrderList"),

    path('orderCompleted/',Rviews.orderCompleted,name="orderCompleted"),
    path('showHistory/',Rviews.showHistory,name="showHistory"),

    path('orderCompleted/<int:orderId>',views.orderCompleted,name="orderCompleted"),        #idk about this

    path('addItemPrompt/',Rviews.addItemPrompt,name="addItemPrompt"),
    path('addMenuItem/',Rviews.addMenuItem,name="addMenuItem"),
    path('showMenuItems/',Rviews.showMenuItems,name="showMenuItems"),

    path('toggleItem/<int:i>',Rviews.toggleItem,name="toggleItem"),
    path('removeItem/<int:i>',Rviews.removeItem,name="removeItem"),



    #---------------extra
    path('getWeight/',views.getWeight,name="getWeight"),
    path('removeWeight/',views.removeWeight,name="removeWeight"),
    path('printBill/',views.printBill,name="printBill"),
    #----------------------------figured it out

]
