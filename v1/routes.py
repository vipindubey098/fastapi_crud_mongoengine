from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Header, Request, Path, Body
from typing import List, Optional, Dict
from v1.serializers import *
from v1.models import *
from pydantic import constr, conint
from datetime import datetime
from blogs_management import *
import json
from mongoengine.queryset.visitor import Q
from v1.jwt_handler import *
from v1.jwt_bearer import *
from pprint import pprint
from users_management import *


router = APIRouter()


# Insert data
@router.post("/addblogs", dependencies=[Depends(jwtBearer())], tags=['Homepage'])
# @router.post("/addblogs", tags=['Homepage'])
async def add_blogs(
    blogs_id: int = Form(None), 
    title: str = Form(...), 
    image_field: Optional[UploadFile] = File(None), 
    description: str = Form(...), 
    category: list = Form(...), 
    tags: list = Form(...)
    ):

    try:
        # fileread for image
        fileread = image_field.file.read()
        # filename for image
        image_filename = image_field.filename
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
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, details=e.message)

# fetch all data
@router.get('/get_all_blogs', dependencies=[Depends(jwtBearer())], tags=['Get All Blogs'])
async def get_blogs(
    req: Request,
    title: str = None, 
    page: int = 1, 
    per_page: int =10, 
    sort_by: str = 'new_as'):
    try:
        skip = (page - 1) * per_page
        limit = per_page
        
        request_args = dict(req.query_params)
        # we will first check data from url whether it contains sort_by or not using request_args
        if request_args.get('sort_by'):
            sort_by = request_args['sort_by']
            # deleting sort_by
            del request_args['sort_by']

        # If i am getting new_as from sort_by then use +created_at else -created_at in query
        sorting_data = "-created_at" if sort_by == "new_as" else "+created_at"

        if title:
            # with the help of __icontains it will help in searching of data
            query = Q(title__icontains=title)
            blogs_list = Blogsdetails.objects(query).order_by(sorting_data).skip(skip).limit(limit)
        else:
            blogs_list = Blogsdetails.objects().order_by(sorting_data).skip(skip).limit(limit)
        return{"blogs": json.loads(blogs_list.to_json())}
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, details=e.message)


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
@router.get('/get_single_blogs/{blogs_id}', dependencies=[Depends(jwtBearer())], tags=['Get All Blogs'])
async def get_single_blogs(blogs_id: int = Path(..., gt=0)):
    # gt means greater than 
    try:
        single_blogs = Blogsdetails.objects.get(blogs_id=blogs_id)
        # testing_data = Blogsdetails.objects(category="string1") 
        # pprint(vars(testing_data))
        # print(testing_data)

        blogs_dict = {
            "blogs_id": single_blogs.blogs_id,
            "title": single_blogs.title,
            "description": single_blogs.description,
            "image_field": single_blogs.image_field,
            "category":single_blogs.category,
            "tags": single_blogs.tags,
            "created_at": single_blogs.created_at
        }

        return blogs_dict
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, details=e.message)


# Update data based on form data
@router.put('/update_blogs_data', dependencies=[Depends(jwtBearer())], tags=['Get All Blogs'])
async def update_blogs_data(blogs_id: int = Form(None), title: str = Form(...), image_field: Optional[UploadFile] = File(None), description: str = Form(...), category: list = Form(...), tags: list = Form(...), created_at: str = Form(...)):
    try:
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
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, detail=e.message)

# delete blogs based on id
@router.delete('/deleteblogs/{blogs_id}', dependencies=[Depends(jwtBearer())], tags=['Get All Blogs'])
async def delete_blogs(blogs_id):
    try:
        blogs_obj = Blogsdetails.objects.get(blogs_id=blogs_id)
        blogs_obj.delete()
        return{'status': "Blogs deleted successfully"}
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, detail=e.message)

# users = []
@router.post("/user/signup", tags=["user"])
def user_signup(user: usersDetail):
# def user_signup(title: str = Form(...), title: str = Form(...), title: str = Form(...)):
    try:
        fullname, email, password = user.fullname, user.email, user.password
        # creating object as we have set_password inside userInsert class
        userInsertObject = userInsert()
        # Now using test.set_password below and passing password as a parameter
        encrypt_pass = userInsertObject.set_password(password=password)
        insertuser = userInsert(full_name=fullname, email=email, password=encrypt_pass)
        insertuser.save()
        return signJWT(user.email)
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    

@router.post("/user/login", tags=["user"])
def user_login(user: checkUserLogin):
    try:
        if not check_user(user):
            return signJWT(user.email)
        else:
            return{"error": "Invalid login details"}
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, detail=e.message)