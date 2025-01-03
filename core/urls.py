from django.urls import path
from .views import HomePageView, trigger_test


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('api/trigger/', trigger_test, name='trigger_test'),

]
