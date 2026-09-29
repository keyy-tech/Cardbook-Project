from django.urls import path

from .views import (
    CreateCardAPIView,
    DestroyCardAPIView,
    RetreivePersonalFullAPIView,
    RetreivePersonalShortAPIView,
    UpdateCardAPIView,
)

urlpatterns = [
    path("card/",RetreivePersonalShortAPIView.as_view()),
    path("card/<int:pk>/",RetreivePersonalFullAPIView.as_view()),
    path("card/create/",CreateCardAPIView.as_view()),
    path("card/update/<int:pk>/",UpdateCardAPIView.as_view()),
    path("card/destroy/<int:pk>/",DestroyCardAPIView.as_view())
]
