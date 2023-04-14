from mongoengine import Document, EmbeddedDocument, StringField, BooleanField, IntField, fields, ListField, EmbeddedDocumentField, DateTimeField, DictField, ImageField
from PIL import Image
import datetime
from pydantic import validator
import logging
from werkzeug.security import generate_password_hash, check_password_hash

    
class userInsert(Document):
    full_name = StringField(max_length=120, required=True)
    email = StringField(max_length=120, required=True)
    password = StringField()

    def payload(self):
        return {
            "fullname": self.full_name,
            "email": self.email,
            "password": self.password
        }

    def set_password(self, password):
        return generate_password_hash(password)
    
    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

class UserLoginSchema(Document):
    # fullname: StringField(max_length=120)
    email: StringField(max_length=120)
    password: StringField()

    def payload(self):
        return {
            "id": str(self.id),
            "full_name": self.fullname,
            "email": self.email
        }


class Blogscategory(EmbeddedDocument):
    # category_id = IntField()
    category_name = StringField(max_length=120)
    # category_description = StringField(null=True)

    def payload(self):
        return {
            "category_name" : self.category_name,
            # "category_description" : self.category_description
        }
    

class Blogstags(EmbeddedDocument):
    # tags_id = IntField()
    tags_name = StringField(max_length=120)

    def payload(self):
        return {
            "tag_name" : self.tags_name
        }

class Blogsdetails(Document):
    # blogs_id = IntField(primary_key=True)
    #using primary_key=True will replace blogs_id using _id
    blogs_id = IntField()
    title = StringField(max_length=120)
    description = StringField(max_length=120)
    image_field = StringField(max_length=120)
    # category = fields.MapField(fields.EmbeddedDocumentField(Blogscategory))
    category = ListField(EmbeddedDocumentField(Blogscategory))
    # tags = fields.MapField(fields.EmbeddedDocumentField(Blogstags))
    tags = ListField(EmbeddedDocumentField(Blogstags))
    # created_at = DateTimeField(default=datetime.datetime.utcnow,required=True)
    
    def payload(self):
        return {
            "id": self.blogs_id,
            "title": self.title,
            "description": self.description,
            "image_field": self.image_field,
            "category": self.category,
            "tags": self.tags,
            # "created_at": self.created_at
        }

   