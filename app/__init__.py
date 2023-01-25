from fastapi import FastAPI
from app.routes import router
from starlette.middleware.cors import CORSMiddleware

main_app = FastAPI()

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
main_app.include_router(router)
