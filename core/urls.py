from django.urls import path
from .views import HomePageView, trigger_test, trigger_test_detail


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('api/trigger/', trigger_test, name='trigger_test'),
    path('trigger/<int:test_id>/', trigger_test_detail, name='trigger_detail'),
]
