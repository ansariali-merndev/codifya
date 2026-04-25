from fastapi import APIRouter
from src.utils import success_res

root_router = APIRouter()


@root_router.get("/")
def root():
    return success_res("Codifya backend server is up and running.")
