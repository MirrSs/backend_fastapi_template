import os


def check_user_image_extension(file_path: str):
    """Check file extension before putting it in db"""
    USER_IMAGE_ALLOWED_EXTENSIONS = (
        '.jpg', '.png', '.jpeg'
    )
    filename, file_extension = os.path.splitext(file_path)
    return file_extension in USER_IMAGE_ALLOWED_EXTENSIONS
