from fastapi import APIRouter

from api.v1.endpoints import products, users, categories, locations

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories & brands"])
api_router.include_router(locations.router, prefix="/locations", tags=["file upload locations (url)"])
