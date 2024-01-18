import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get("DEBUG", "False") == "True"
ROOT_PATH = "/api"

# AUTH
ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "secret")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY", "secret")

# SERVICES
DATABASE_URI = os.getenv("DATABASE_URI")
COGNITO_REGION = os.getenv("AWS_COGNITO_REGION")
COGNITO_USER_POOL_ID = os.getenv("AWS_USER_POOLS_ID")
COGNITO_CLIENT_ID = os.getenv("AWS_USER_POOLS_WEB_CLIENT_ID")

# MISC
FRONTEND_URL = os.getenv("FRONTEND_URL")
