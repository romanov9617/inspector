from rest_framework.routers import SimpleRouter

from admin.settings import REGULAR_API_PREFIX
from admin_modules.media.views import ImageViewSet

router = SimpleRouter()
router.register(f"{REGULAR_API_PREFIX}media", ImageViewSet)

urlpatterns = router.urls
