from rest_framework.routers import SimpleRouter

from admin.settings import REGULAR_API_PREFIX
from admin_modules.defects.views import DefectVersionViewSet
from admin_modules.defects.views import DefectViewSet

router = SimpleRouter()
router.register(f"{REGULAR_API_PREFIX}defect", DefectViewSet)
router.register(f"{REGULAR_API_PREFIX}defect-version", DefectVersionViewSet)

urlpatterns = router.urls
