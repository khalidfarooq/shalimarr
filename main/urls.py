from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('drive/', drive_page,name="drive"),
    path('delete/<str:id>', delete_file),
    path('view/<str:id>', view_file),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('trustee/', trustee, name='trustee'),
    path("thanks/",thanks,name="thanks")
]
