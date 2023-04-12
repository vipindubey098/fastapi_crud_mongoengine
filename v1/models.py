from mongoengine import Document, EmbeddedDocument, StringField, BooleanField, IntField, fields, ListField, EmbeddedDocumentField, DateTimeField, DictField, ImageField
from PIL import Image
from datetime import datetime
from pydantic import validator
import logging


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
    blogs_id = IntField(primary_key=True)
    title = StringField(max_length=120)
    description = StringField(max_length=120)
    image_field = StringField(max_length=120)
    # category = fields.MapField(fields.EmbeddedDocumentField(Blogscategory))
    category = ListField(EmbeddedDocumentField(Blogscategory))
    # tags = fields.MapField(fields.EmbeddedDocumentField(Blogstags))
    tags = ListField(EmbeddedDocumentField(Blogstags))
    # created_at = DateTimeField(default=datetime.now)

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
    