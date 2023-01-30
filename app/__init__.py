from fastapi import FastAPI
from app.routes import router
from starlette.middleware.cors import CORSMiddleware
from config import index_html_url

main_app = FastAPI()

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=[index_html_url],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
main_app.include_router(router)
