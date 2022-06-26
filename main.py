from fastapi import FastAPI
from microblog.app import microblog
from auth.app import auth


app = FastAPI()
app.include_router(microblog)
app.include_router(auth)
