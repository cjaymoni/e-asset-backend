from fastapi import APIRouter, Depends, HTTPException, Request
from dependencies import get_db, validate_bearer
from datetime import timedelta, datetime
from utils import create_jwt, decode_jwt
from rds.tasks import async_send_email
from utils import raise_exc, urljoin
from sqlalchemy.orm import Session
from . import schemas, crud
from config import settings

router = APIRouter()

@router.post('/login', response_model=schemas.LoginResponse, name='Login')
async def authenticate(data:schemas.Login, account:schemas.Account, db:Session=Depends(get_db)):
    user = await crud.verify_user(payload, account, db)

    if not user.is_active:
        raise HTTPException(status_code=417, detail="account is not active")

    if not user.is_verified:
        raise HTTPException(status_code=417, detail="account is not verified")

    data = {"id":user.id}
    if account.value=="users":
        data.update({"role_id":user.role.id})

    # make sure tenant checks

    return {
        "access_token":create_jwt(data=data, exp=timedelta(minutes=settings.ACCESS_TOKEN_DURATION_IN_MINUTES)),
        "refresh_token":create_jwt(data=data, exp=timedelta(minutes=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)),
        "account":account.value,
        "user":data
    }

@router.post("/logout", name='Logout')
async def logout(payload:schemas.Logout, db:Session=Depends(get_db)):
    return await crud.revoke_token(payload, db)

@router.post("/token/refresh", response_model=schemas.Token, name='Refresh Token')
async def refresh_token(payload:schemas.RefreshToken, db:Session=Depends(get_db)):
    if await crud.is_token_blacklisted(payload.refresh_token, db):
        raise HTTPException(status_code=401, detail=raise_exc("refresh_token","token blacklisted","BlacklistedToken"))
    
    if await crud.revoke_token(payload, db):
        data = decode_jwt(token=payload.refresh_token)
        return {
            "access_token":create_jwt(data=data, exp=timedelta(minutes=settings.ACCESS_TOKEN_DURATION_IN_MINUTES)),
            "refresh_token":create_jwt(data=data, exp=timedelta(minutes=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)),
        }

    raise HTTPException(status_code=417)

@router.get('/current-user', response_model=schemas.User, name='JWT User')
async def get_current_user(data:str=Depends(validate_bearer), db:Session=Depends(get_db)):
    return await crud.read_by_id(data['user']['id'], data['account'], db)

@router.post("/send-email-verification-code", name='Request Email verification code')
async def request_email_verification_code(payload:schemas.EmailBase, account:schemas.Account, db:Session=Depends(get_db)):
    obj = await crud.add_email_verification_code(payload.email, account, db)
    crud.schedule_del_code(obj.email)
    if async_send_email(mail={
        "subject":"Email Verification",
        "recipients":[obj.email],
        "body":f"your verification code is: {obj.code}",
        "template_name":"email.html"
    }):return 'you will receive code shortly'
    raise HTTPException(status_code=417)

@router.post('/send-forgot-password-link', name='Request Forgot Password link')
async def forgot_password(request:Request, payload:schemas.EmailBase, account:schemas.Account, db:Session=Depends(get_db)):
    user = await crud.read_by_email(payload.email, account, db)
    if user:
        data = {"id":user.id, "account":account.value}
        token = create_jwt(data, exp=settings.PASSWORD_RESET_TOKEN_DURATION_IN_MINUTES)
        if async_send_email(mail={
            "subject":"Forgot Password",
            "recipients":[obj.email],
            "body":f"your password reset link is: {urljoin(request.base_url, settings.VERIFICATION_PATH)}" 
        }):return 'you will receive link shortly'
        raise HTTPException(status_code=417)
    raise HTTPException(status_code=404, detail=raise_exc("email", "user not found", "NotFound"))