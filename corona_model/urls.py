from django.conf.urls.static import static
# from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from . import views
from django.conf import settings


urlpatterns = [
    # path('', views.index, name='index'),
    path('model3', views.model3_test, name='model3'),
    path('test', views.test, name='test'),
    path('post_test', views.post_test, name='post_test2'),

    path('testview', views.TestView.as_view(), name='testview'),
    
    path('about', views.AboutView.as_view(), name='about'),
    path('predict/<model_number>/', views.Predict.as_view(), name='predict')

]