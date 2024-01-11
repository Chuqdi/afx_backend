from beanie import init_beanie
from fastapi import FastAPI
from mangum import Mangum
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from src.api.health_check import router as health_check_router
from src.config import DATABASE_URI, ROOT_PATH


app = FastAPI(
    title="Affirmatrix API",
    description="This is the documentation for the Affirmatrix API.",
    version="0.0.1",
    terms_of_service="http://polarfrequency.com/",
    contact={
        "name": "POLAR FREQUENCY LLC-FZ",
        "url": "http://polarfrequency.com",
        "email": "admin@polarfrequency.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url=f"{ROOT_PATH}/docs",
    redoc_url=f"{ROOT_PATH}/redoc",
    openapi_url=f"{ROOT_PATH}/openapi.json",
)


origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.on_event("startup")
async def startup_db_client():
    client = AsyncIOMotorClient(DATABASE_URI)
    database = client.dev
    await init_beanie(database, document_models=[])


app.include_router(health_check_router, prefix=f"{ROOT_PATH}/health")

handler = Mangum(app)
