from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('post_statistics/', include('post_statistics.urls'))
]
