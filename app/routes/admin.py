from app.models.user_models import User
from app.services.admin import AdminService
from app.schemas.user import GenericResponseModel
from app.schemas.admin import AdminGetUserProfileOut, AdminProfileResponseWrapper, AdminRole, AdminAuthResponse, AdminProfileModel, AdminLogin,AdminProfileResponse, AdminRegister
from db import SessionLocal
from db import get_db
from fastapi import APIRouter, Depends, status, Form, File, UploadFile
from typing import Union, Optional
from sqlalchemy.orm import Session

admin_router = APIRouter(prefix="/admin", tags=['Admin'])
@admin_router.get("/list/users", response_model=Union[AdminGetUserProfileOut, GenericResponseModel])
def get_all_users_profile(db: Session = Depends(get_db), token: str = Depends(AdminService.oauth2_scheme)):
    admin_service = AdminService(db)
    return admin_service.get_all_users(token=token, db=db)


@admin_router.post("/register", response_model=Union[AdminAuthResponse, GenericResponseModel])
def register(user: AdminRegister, db: Session = Depends(get_db)):
    admin_service = AdminService(db)
    return admin_service.register_user(user)

@admin_router.post("/login", response_model=Union[AdminAuthResponse, GenericResponseModel])
def login(user: AdminLogin, db: Session = Depends(get_db)):
    admin_service = AdminService(db)
    return admin_service.login_user(user)

@admin_router.put("/profile/update", response_model = GenericResponseModel[AdminProfileResponse])
def update_profile(
    username: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None),
    avi: Optional[UploadFile] = File(None),
    token: str = Depends(AdminService.oauth2_scheme),
    db: Session = Depends(get_db)
):
    service = AdminService(db)
    return service.update_profile(
        user_data=AdminProfileModel(username=username,full_name = full_name),
        token = token,
        db=db,
        avi_file = avi
        )

@admin_router.get(
    "/profile/me",
    response_model=AdminProfileResponseWrapper
)
def get_profile(current_user: User = Depends(AdminService.get_current_admin_user)):
    return {
        "message": "Profile fetched successfully!",
        "data": {
            "uuid": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
            "username": current_user.username,
            "full_name": current_user.full_name,
            "avi": current_user.avi,
            "is_active": current_user.is_active
        }
    }


# @router.post("/logout", response_model=Union[GenericResponseModel, AuthResponse])
# def logout(token: str = Depends(UserService.oauth2_scheme), db: Session = Depends(get_db)):
#     service = UserService(db)
#     return service.logout_user(token=token, db=db)

# @router.post("/refresh")
# def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
#     service = TokenService(db)
#     return service.refresh_token(request.refresh_token)
