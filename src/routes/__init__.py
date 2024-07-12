from fastapi import APIRouter
from .test_router import test_router

router = APIRouter()

router.include_router(test_router)
