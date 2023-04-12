from v1.models import *
import os
from fastapi import File, UploadFile
import shutil
import logging
from exception_handler import *

class BlogsHandler:
    def __init__(self) -> None:
        # creating image folder
        self.blogging_image = None
        self.image_field = os.path.join(os.getcwd(), "blogs_image")
        if not os.path.exists(self.image_field):
            os.makedirs(self.image_field)
        
    # function to save blogsimage
    def saveBlogsImage(image_name: File):
        try:
            image_field = os.path.join(os.getcwd(), "blogs_image")
            if not os.path.exists(image_field):
                os.makedirs(image_field)
            file_location= image_field+'/'+image_name.filename
            with open(file_location, "wb+") as file_object:
                file_object.write(image_name.file.read())
                shutil.copyfileobj(image_name.file, file_object)
        except Exception as e:
            logging.error(e)
            raise CustomExceptionHandler(code=500, message="Internal Server Error")