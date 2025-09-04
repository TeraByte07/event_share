from app.models.user_models import User
from app.services.user import UserService,TokenService
from app.schemas.user import UserLogin,ProfileModel, UserRegister, RefreshTokenRequest,UserRole, GenericResponseModel,AuthResponse, ProfileResponseWrapper, ProfileResponse
from db import SessionLocal
from db import get_db
from fastapi import APIRouter, Depends, status, Form, File, UploadFile
from typing import Union, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=['Auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=Union[AuthResponse, GenericResponseModel])
def register(user: UserRegister, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.register_user(user)

@router.post("/login", response_model=Union[AuthResponse, GenericResponseModel])
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.login_user(user)

@router.put("/profile/update", response_model=GenericResponseModel[ProfileResponse])
def update_profile(
    username: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None),
    avi: Optional[UploadFile] = File(None),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service.update_profile(
        user_data=ProfileModel(username=username, full_name=full_name),
        token=token,
        db=db,
        avi_file=avi,
    )


@router.get("/profile/me", response_model=ProfileResponseWrapper)
def get_profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service.get_user_profile(token=token, db=db)


@router.post("/logout", response_model=Union[GenericResponseModel, AuthResponse])
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    service = UserService(db)
    return service.logout_user(token=token, db=db)

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    service = TokenService(db)
    return service.refresh_token(request.refresh_token)