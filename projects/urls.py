from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageAPIView, ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # path("api/contact/", ContactMessageViewSet.as_view, name="contact-create"),
     path("api/contact/", ContactMessageAPIView.as_view(), name="contact"),
]
