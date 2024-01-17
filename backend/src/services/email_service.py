import smtplib
from settings import SENDER_EMAIL, SMTP_ADDRESS, SMTP_PORT, CONFIRMATION_URL
from managers.user_manager import UserManager
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service import AuthService
import json

class EmailService:

    confirmation_letter = """
     To confirm your registration,
     please click on link:
     """

    @classmethod
    async def send_email(cls, receiver: str, message: str):
        try:
            smtpObj = smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT)
            smtpObj.sendmail(SENDER_EMAIL, receiver, message)
            print("Successfully sent email")
        except smtplib.SMTPException:
            print("Error: unable to send email")


    @classmethod
    async def generate_confirmation_url(cls, receiver: str, session: AsyncSession) -> str:
        user = await UserManager.retrieve(email=receiver, session=session)
        token = await AuthService.create_token(user.id, 'access')
        return f'{CONFIRMATION_URL}{str(token)}'


    @classmethod
    async def confirm_user(cls, token: str, session: AsyncSession) -> str:
        user_id = AuthService.decode_token(token=token)
        update_dict = {
            'is_active': True
        }
        await UserManager.update(
            session=session, pk=user_id, input_data=update_dict
        )
        return {'detail':"User confirmed successfully"}
