from auth.models import User


DATABASE_URL = 'postgresql+psycopg2://postgres:POSTGRES@localhost:5432/postgres'
TEST_DATABASE_URL = 'postgresql+psycopg2://postgres:POSTGRES@localhost:5432/pytest'
MEDIA_URL = 'media/'
SECRET_KEY = 'ABCD'
USER_MODEL = User
USER_FIELD = 'user_id'
