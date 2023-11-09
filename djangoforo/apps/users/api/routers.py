from rest_framework.routers import DefaultRouter
from .viewsets import (
    UserGenericViewSet,
    UsersViewSet
)


router = DefaultRouter()

router.register('userslol', UserGenericViewSet, 'userslol')
router.register('userview', UsersViewSet, 'userviews')

urlpatterns = router.urls