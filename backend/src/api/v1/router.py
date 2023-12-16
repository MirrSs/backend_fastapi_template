from fastapi import APIRouter


from api.v1.user_router import user_router
from api.v1.auth_router import auth_router

api_v1 = APIRouter(prefix='/v1')

#Add your routers here
api_v1.include_router(user_router)
api_v1.include_router(auth_router)

