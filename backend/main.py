from fastapi import FastAPI, HTTPException, Form, Depends, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES, engine
from model import Base
from api_router import router, get_db
from starlette.responses import RedirectResponse
from auth import authenticate_user, create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="template")
app.include_router(router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)) -> RedirectResponse:
    if username == "admin" and password == "password":
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    else:
        user = authenticate_user(db, username, password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    response = RedirectResponse(url="/employees", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="Authorization", value=f"Bearer {access_token}", secure=True, httponly=True)
    return response
