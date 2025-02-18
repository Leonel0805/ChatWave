from rest_framework.routers import DefaultRouter
from .viewsets import (
    UserGenericViewSet,
)


router = DefaultRouter()

router.register('usersview', UserGenericViewSet, 'usersview')

urlpatterns = router.urls