from rest_framework.routers import SimpleRouter

from admin.settings import REGULAR_API_PREFIX
from admin_modules.ml_models.views import MLModelViewSet

router = SimpleRouter()
router.register(f"{REGULAR_API_PREFIX}model", MLModelViewSet)

urlpatterns = router.urls
