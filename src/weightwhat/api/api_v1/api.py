from fastapi import APIRouter

from .endpoints.ping import router as ping_router
from .endpoints.weights import router as weights_router


router = APIRouter()
router.include_router(ping_router)
router.include_router(weights_router)
