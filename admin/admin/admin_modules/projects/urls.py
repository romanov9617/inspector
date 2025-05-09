from rest_framework.routers import SimpleRouter

from admin.settings import REGULAR_API_PREFIX
from admin_modules.projects.views import ProjectViewSet

router = SimpleRouter()
router.register(f"{REGULAR_API_PREFIX}project", ProjectViewSet)

urlpatterns = router.urls
