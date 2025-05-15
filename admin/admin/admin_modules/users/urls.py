from rest_framework.routers import SimpleRouter

from admin.settings import REGULAR_API_PREFIX
from admin_modules.users.views import CustomUserViewSet

router = SimpleRouter()
router.register(f"{REGULAR_API_PREFIX}auth/users", CustomUserViewSet)

urlpatterns = router.urls
