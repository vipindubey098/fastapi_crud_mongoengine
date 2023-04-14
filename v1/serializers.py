from pydantic import BaseModel, validator, root_validator
from typing import List, Optional, Dict
from datetime import datetime
import logging


class BlogsModels(BaseModel):
    blogs_id : int
    title : Optional[str]
    description : Optional[str]
    image_field : Optional[str]
    category : Optional[list]
    tags : Optional[list]
    # created_at : datetime = datetime.now()

    

    class Config:
        arbitrary_types_allowed = True

    # @validator('category')
    # def category_must_have_unique_name(cls, values):
    #     category_names = []
    #     for item in values:
    #         category_names.append(item.category)
    #     if len(category_names) > len(set(category_names)):
    #         raise ValueError('must contain unique names')
    #     return values


    # @validator('tags', pre=True)
    # def validate_tags(cls, v):
    #     if isinstance(v, List):
    #         return v
    #     elif isinstance(v, str):
    #         return [v]
    #     else:
    #         raise ValueError(f'Invalid values: {v}')


class TagsModels(BaseModel):
    # tags_id = int
    tags_title = Optional[str]

    class Config:
        arbitrary_types_allowed = True

class CategoryModels(BaseModel):
    # category_id = int
    category_title = Optional[str]
    # category_description = Optional[str]

    class Config:
        arbitrary_types_allowed = True


class usersDetail(BaseModel):
    fullname: str
    email: str
    password: str
    
    class Config:
        arbitrary_types_allowed = True

class checkUserLogin(BaseModel):
    # fullname: str
    email: str
    password: str

    class Config:
        arbitrary_types_allowed = True