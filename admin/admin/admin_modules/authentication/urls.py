from rest_framework.routers import SimpleRouter

from admin.settings import REGULAR_API_PREFIX
from admin_modules.authentication.views import UserViewSet

router = SimpleRouter()
router.register(f"{REGULAR_API_PREFIX}user", UserViewSet)

urlpatterns = router.urls
