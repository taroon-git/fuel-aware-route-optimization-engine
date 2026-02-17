from django.urls import path
from .views import home, route_optimizer

urlpatterns = [
    path('', home, name='home'),
    path('api/route/', route_optimizer, name='route_optimizer'),
]
