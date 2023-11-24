from rest_framework.routers import DefaultRouter
from .viewsets import RoomGenericViewSet


router = DefaultRouter()

router.register('', RoomGenericViewSet, 'roomsviewset')

urlpatterns = router.urls