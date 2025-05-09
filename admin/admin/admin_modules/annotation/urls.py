from rest_framework.routers import SimpleRouter

from admin.settings import REGULAR_API_PREFIX
from admin_modules.annotation.views import AnnotationSessionViewSet

router = SimpleRouter()
router.register(f"{REGULAR_API_PREFIX}annotation", AnnotationSessionViewSet)

urlpatterns = router.urls
