from celery import Celery, shared_task
from celery.schedules import crontab
import io
from services.email_service import EmailService
from services.minio_service import MinioService


app = Celery('tasks', broker='redis://redis:6379')

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Executes every Monday morning at 10:00 a.m.
#     sender.add_periodic_task(
#         crontab(hour=10, minute=0, day_of_week=1),
#         notify_users.s(),
#     )

@shared_task
def upload_user_profile_image(object_name:str, data:dict):
    img = io.BytesIO(data.get('file'))
    
    msg, status_code = MinioService.upload_file(
        file=img,
        filename=data.get('name'),
        size=data.get('size'),
        content_type=data.get('content_type'),
        object_name=object_name,
    )
    print(f'Minio:{msg}')
    print(f'Status:{status_code}')

@app.task
def send_registration_confirmation_letter(email: str,message: str):
    EmailService.send_email(
        receiver=email, message=message
    )
