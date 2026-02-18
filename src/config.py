import os

API_TOKEN_EXPIRATION_HOURS = int(os.getenv("API_TOKEN_EXPIRATION_HOURS", "12"))
API_TOKEN_SECRET = os.getenv("API_TOKEN_SECRET", "aidjfaoijfididid")
SECONDS_TO_EXPIRE_USER_STATE = int(os.getenv("SECONDS_TO_EXPIRE_USER_STATE", "60"))

WEB_GOOGLE_CLIENT_ID = os.environ.get("WEB_GOOGLE_CLIENT_ID", "android_client_id")
WEB_GOOGLE_REDIRECT_URI = os.environ.get("WEB_GOOGLE_REDIRECT_URI", "redirect_uri")
WEB_GOOGLE_SECRET = os.environ.get("WEB_GOOGLE_SECRET", "")

HOURS_TO_EXPIRATION_TOKEN = int(os.getenv("HOURS_TO_EXPIRATION_TOKEN", "720"))
SECONDS_TO_VALID = 0

JWT_ALGORITHM = "HS256"
JWT_REQUIRED_CLAIMS = ['exp', 'iat', 'nbf', 'sub']


DB_USERNAME = os.getenv("DB_USERNAME", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "app_db_name")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_CONNECTION_STR = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

FILE_REPOSITORY = os.getenv("FILE_REPOSITORY", ".files")
TEMP_FILE_REPOSITORY_DIRECTORY = os.path.join(FILE_REPOSITORY, "temp")

# if you will allow cors outside (nginx for example) it should be false to avoid duplicate headers
ADD_ALLOW_CORS = os.getenv("ADD_ALLOW_CORS", "false") == "true"