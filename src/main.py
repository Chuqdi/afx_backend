from beanie import init_beanie
from fastapi import FastAPI
from mangum import Mangum
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from src.api.health_check import router as health_check_router
from src.api.affirmation import router as affirmation_router
from src.api.auth import router as auth_router
from src.config import DATABASE_URI, ROOT_PATH
from src.models.affirmation import Affirmation
from src.models.affirmation_background_sound import AffirmationBackgroundSound
from src.models.affirmation_listening_history import AffirmationListeningHistory
from src.models.affirmation_package import AffirmationPackage
from src.models.affirmation_package_field import AffirmationPackageField
from src.models.affirmation_statistic import AffirmationStatistic
from src.models.affirmation_voice import AffirmationVoice
from src.models.billing_history import BillingHistory
from src.models.field import Field
from src.models.payment import UsedPaymentIntent, UserPaymentMethod
from src.models.stripe import StripePrice, StripeProduct
from src.models.subscription import Subscription
from src.models.user_affirmation_package_field import UserAffirmationPackageField
from src.models.user_crediting_system import UserCreditingSystem


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
    await init_beanie(
        database,
        document_models=[
            Affirmation,
            AffirmationPackage,
            AffirmationPackageField,
            UserAffirmationPackageField,
            AffirmationBackgroundSound,
            AffirmationVoice,
            AffirmationListeningHistory,
            AffirmationStatistic,
            BillingHistory,
            Field,
            Subscription,
            UserPaymentMethod,
            UsedPaymentIntent,
            UserCreditingSystem,
            StripeProduct,
            StripePrice,
        ],  # type: ignore
    )


app.include_router(health_check_router, prefix=f"{ROOT_PATH}/health")
app.include_router(auth_router, prefix=f"{ROOT_PATH}/auth", tags=["Auth"])
app.include_router(
    affirmation_router, prefix=f"{ROOT_PATH}/affirmations", tags=["Affirmation"]
)


handler = Mangum(app)
