from django.urls import path,include
from .views import *

urlpatterns = [
    path('file', FileAPIView.as_view()),
    path('file/<str:fid>', FileOperations.as_view()),

]
