from django.urls import path
from users.views import LoginAPIView, SignupViewSet

urlpatterns = [
    path('signup/', SignupViewSet.as_view()),
    path('token/', LoginAPIView.as_view()),
]
