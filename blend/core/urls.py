from django.urls import path
from .views import index , user , compare_users , generate_common_list

urlpatterns = [
    path('' , index , name = "home"),
    path('user/', user ,name = "user" ),
    path('compare/' , compare_users , name = "compare"),
    path('common_list' , generate_common_list , name = "common_list")
]
