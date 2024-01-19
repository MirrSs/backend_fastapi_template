from celery import Celery
from fastapi import UploadFile
from celery.schedules import crontab
from services.email_service import EmailService
from services.minio_service import MinioService
from PIL import Image

app = Celery('tasks', broker='redis://redis:6379')

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Executes every Monday morning at 10:00 a.m.
#     sender.add_periodic_task(
#         crontab(hour=10, minute=0, day_of_week=1),
#         notify_users.s(),
#     )

@app.task
def resize_and_upload_user_profile_image(object_name:str, file:UploadFile):
    image = Image.open(file)
    resized_image = image.resize(600,600)
    msg, status_code = MinioService.upload_file(
        file=resized_image,
        object_name=object_name
    )
    print(msg)
    print(status_code)

@app.task
def send_registration_confirmation_letter(email: str,message: str):
    EmailService.send_email(
        receiver=email, message=message
    )

@app.task
def add(x, y):
    return x + y