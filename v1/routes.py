from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Header, Request, Path, Body
from typing import List, Optional, Dict
from v1.serializers import *
from v1.models import *
from pydantic import constr, conint
from datetime import datetime
from blogs_management import *
import json
from mongoengine.queryset.visitor import Q


router = APIRouter()


# Insert data
@router.post("/addblogs", tags=['Homepage'])
async def add_blogs(blogs_id: int = Form(None), title: str = Form(...), image_field: Optional[UploadFile] = File(None), description: str = Form(...), category: list = Form(...), tags: list = Form(...)):

    # fileread for image
    fileread = image_field.file.read()
    # filename for image
    image_filename = image_field.filename
    # print(image_filename)
    print(type(blogs_id))
    new_blogs = Blogsdetails(blogs_id=blogs_id, title=title, description=description, image_field=image_filename)
    for data in category:
        data = data.replace("[]","").replace("]","").split(",")
        for record in data:
            category__ = Blogscategory(category_name=record)
            new_blogs.category.append(category__)


    for data_tags in tags:
        data1 = data_tags.replace("[]","").replace("]","").split(",")
        for record_data in data1:
            tags__ = Blogstags(tags_name=record_data)   
            new_blogs.tags.append(tags__)

    if image_field is not None:
        response = BlogsHandler.saveBlogsImage(image_name=image_field)
    new_blogs.save()

    return{"message":"Blogs Added Successfully"}

# fetch all data
@router.get('/get_all_blogs')
def get_blogs(title: str = None, page: int = 1, per_page: int =10):
    skip = (page - 1) * per_page
    limit = per_page
    if title:
        # with the help of __icontains it will help in searching of data
        query = Q(title__icontains=title)
        blogs_list = Blogsdetails.objects(query).skip(skip).limit(limit)
    else:
        blogs_list = Blogsdetails.objects().skip(skip).limit(limit)
    return{"blogs": json.loads(blogs_list.to_json())}


# Multiple query based on search
# async def get_users(q: str = None, age: int = None, page: int = 1, per_page: int = 10):
#     query = {}
#     if q:
#         query |= Q(name_icontains=q) | Q(email_icontains=q)
#     if age:
#         query |= Q(age=age)
#     skip = (page - 1) * per_page
#     limit = per_page
#     users = User.objects(**query).skip(skip).limit(limit)
#     return users.to_json()


# fetch blogs based on blogs_id
@router.get('/get_single_blogs/{blogs_id}')
def get_single_blogs(blogs_id: int = Path(..., gt=0)):
    # gt means greater than 
    single_blogs = Blogsdetails.objects.get(blogs_id=blogs_id)

    blogs_dict = {
        "blogs_id": single_blogs.blogs_id,
        "title": single_blogs.title,
        "description": single_blogs.description,
        "image_field": single_blogs.image_field,
        "category":single_blogs.category,
        "tags": single_blogs.tags
    }

    return blogs_dict


# Update data based on form data
@router.put('/update_blogs_data')
def update_blogs_data(blogs_id: int = Form(None), title: str = Form(...), image_field: Optional[UploadFile] = File(None), description: str = Form(...), category: list = Form(...), tags: list = Form(...)):
    # fileread for image
    fileread = image_field.file.read()
    # filename for image
    image_filename = image_field.filename
    
    if image_field is not None:
        response = BlogsHandler.saveBlogsImage(image_name=image_field)
    Blogsdetails.objects(blogs_id=blogs_id).update(title=title, description=description, image_field=image_filename)
    blogs_category = []
    for data in category:
        data = data.replace("[]","").replace("]","").split(",")
        for record in data:
            category__ = Blogscategory(category_name=record)
            blogs_category.append(category__)
            Blogsdetails.objects(blogs_id=blogs_id).update(category=blogs_category)

    blogs_tags = []
    for data_tags in tags:
        data1 = data_tags.replace("[]","").replace("]","").split(",")
        for record_data in data1:
            tags__ = Blogstags(tags_name=record_data)   
            blogs_tags.append(tags__)
            Blogsdetails.objects(blogs_id=blogs_id).update(tags=blogs_tags)

    return{"message":"Blogs Updated Successfully"}


# delete blogs based on id
@router.delete('/deleteblogs/{blogs_id}')
async def delete_blogs(blogs_id):
    blogs_obj = Blogsdetails.objects.get(blogs_id=blogs_id)
    blogs_obj.delete()
    return{'status': "Blogs deleted successfully"}