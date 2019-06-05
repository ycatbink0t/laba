from django.urls import include, path
from . import views


urlpatterns = [
    path('main/', views.main),
    path('api/', views.api),
    path('adduserform/', views.adduser_form),
    path('addstreetform/', views.addstreet_form),
    path('login/', views.login_page),
    path('auth/', views.auth),
    path('registration/', views.registration_page),
    path('reg/', views.reg),
    path('logout/', views.lgout)
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()