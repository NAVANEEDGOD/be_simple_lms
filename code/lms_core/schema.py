from ninja import Schema
from typing import Optional
from datetime import date, datetime

from django.contrib.auth.models import User

# Category UAS

# schemas.py

class CategoryIn(Schema):
    name: str

class CategoryOut(Schema):
    id: int
    name: str
    creator_id: int

# Category UAS




class UserOut(Schema):
    id: int
    email: str
    first_name: str
    last_name: str


class CourseOut(Schema):
    id: int
    name: str
    description: str
    price: int
    image : Optional[str]
    teacher: UserOut
    created_at: datetime
    updated_at: datetime

class CourseMemberOut(Schema):
    id: int 
    course_id: CourseOut
    user_id: UserOut
    roles: str
    # created_at: datetime


class CourseIn(Schema):
    name: str
    description: str
    price: int
    category_id: int 


class CourseContentMini(Schema):
    id: int
    name: str
    description: str
    course_id: CourseOut
    created_at: datetime
    updated_at: datetime


class CourseContentFull(Schema):
    id: int
    name: str
    description: str
    video_url: Optional[str]
    file_attachment: Optional[str]
    course_id: CourseOut
    created_at: datetime
    updated_at: datetime

class CourseCommentOut(Schema):
    id: int
    content_id: CourseContentMini
    member_id: CourseMemberOut
    comment: str
    created_at: datetime
    updated_at: datetime

class CourseCommentIn(Schema):
    comment: str

# FeedBack UAS

class FeedbackIn(Schema):
    course_id: int
    message : str
    rating: int

class FeedbackOut(Schema):
    id: int
    course_id: int
    user_id: int
    message: str
    rating: int
    created_at: datetime

# FeedBack UAS

# Bookmark UAS

class BookmarkIn(Schema):
    course_id : int
    content_id : int

class BookmarkOut(Schema):
    id:int
    user_id:int
    course_id:int
    content_id:int

# Bookmark UAS

# Announcment UAS

class AnnouncementIn(Schema):
    course_id: int
    title: str
    content: str
    publish_date: date

class AnnouncementOut(Schema):
    id: int
    course_id: int
    title: str
    content: str
    publish_date: date

# Announcment UAS

