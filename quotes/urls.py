from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [path('',views.home,name='home'),path('author/<int:pk>/',views.author_detail,name='author'),path('register/',views.register,name='register'),path('login/',auth_views.LoginView.as_view(template_name='quotes/form.html',extra_context={'title':'Вхід'}),name='login'),path('logout/',auth_views.LogoutView.as_view(),name='logout'),path('author/add/',views.add_author,name='add_author'),path('quote/add/',views.add_quote,name='add_quote'),path('scrape/',views.scrape_import,name='scrape')]
