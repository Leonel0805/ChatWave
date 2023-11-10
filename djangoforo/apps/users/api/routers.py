from rest_framework.routers import DefaultRouter
from .viewsets import (
    UserGenericViewSet,
    UsersViewSet
)


router = DefaultRouter()

router.register('usersview', UserGenericViewSet, 'userslol')
router.register('userviewset', UsersViewSet, 'userviews')

urlpatterns = router.urls