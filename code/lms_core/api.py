from typing import List
from ninja import NinjaAPI, UploadedFile, File, Form
from ninja.responses import Response
from lms_core.schema import AnnouncementIn, AnnouncementOut, BookmarkIn, BookmarkOut, CategoryIn, CategoryOut, CourseIn, CourseOut, CourseMemberOut, FeedbackIn, FeedbackOut
from lms_core.schema import CourseContentMini, CourseContentFull
from lms_core.schema import CourseCommentOut, CourseCommentIn
from lms_core.models import Announcement, Bookmark, Category, Course, CourseMember, CourseContent, Comment, Feedback
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja.pagination import paginate, PageNumberPagination


from django.contrib.auth.models import User

from lms_core.views import  allCourse, courseById 

apiAuth = HttpJwtAuth()
apiv1 = NinjaAPI()
apiv1.add_router("/auth/", mobile_auth_router)

# Course
@apiv1.get("/courses")
def getAllCourses(request):
    return allCourse(request)

@apiv1.get("/course/{course_id}",auth = apiAuth)
def getCourseById(request,course_id: int):
    return courseById(request,course_id)

@apiv1.post("/add-course", response=CourseOut , auth = apiAuth)
def create_course(request, payload: CourseIn):

    # ini untuk sementara testing dimana butuh authtentikasi 
    if not request.user.is_authenticated:
        request.user = User.objects.first()
    # ini untuk sementara testing dimana butuh authtentikasi 

    course = Course.objects.create(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        teacher=request.user,  # asumsi teacher = user yang login
        category_id=payload.category_id
    )
    return course

@apiv1.put("/update-course/{course_id}", response=CourseOut , auth = apiAuth)
def update_course(request, course_id: int, payload: CourseIn):

    # ini untuk sementara testing dimana butuh authtentikasi 
    if not request.user.is_authenticated:
        request.user = User.objects.first()
    # ini untuk sementara testing dimana butuh authtentikasi 

    course = Course.objects.get(id=course_id, teacher=request.user)
    # try:
    # except Course.DoesNotExist:
    #     raise HttpError(404, "Course not found or unauthorized")
    category = Category.objects.get(id = payload.category_id)

    course.name = payload.name
    course.description = payload.description
    course.price = payload.price
    course.category = category
    course.save()

    return course

@apiv1.delete("/delete-course/{course_id}" , auth = apiAuth)
def delete_course(request, course_id: int):


    course = Course.objects.get(id=course_id, teacher=request.user)
    course.delete()
    return {"success": True, "message": "Course deleted"}

# UAS

# FEEDBACK

@apiv1.get("/feedback/{course_id}", response=List[FeedbackOut] , auth = apiAuth)
def show_feedback(request, course_id: int):
    feedbacks = Feedback.objects.filter(course_id=course_id)
    return feedbacks

@apiv1.post("/add-feedback", response=FeedbackOut , auth = apiAuth)
def add_feedback(request, payload: FeedbackIn):
    course = Course.objects.get(id=payload.course_id)
    user = User.objects.get(id=request.user.id)
    feedback = Feedback.objects.create(
        course=course,
        user=user,  # pastikan pakai authentication
        message=payload.message,
        rating=payload.rating
    )
    return feedback

@apiv1.put("/update-feedback/{feedback_id}", response=FeedbackOut , auth = apiAuth)
def update_feedback(request, feedback_id: int, payload: FeedbackIn):
    feedback = Feedback.objects.get(id=feedback_id)
    course = Course.objects.get(id=payload.course_id)
    feedback.message = payload.message
    feedback.rating = payload.rating
    feedback.course = course
    feedback.save()

    return feedback

@apiv1.delete("/delete-feedback/{feedback_id}" , auth = apiAuth)
def delete_feedback(request, feedback_id: int):
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.delete()
    return {"success": True, "message": "Feedback deleted"}

# Bookmark
@apiv1.get("/bookmark", response=List[BookmarkOut] , auth = apiAuth)
def show_bookmarks(request):
    return Bookmark.objects.filter(user_id=request.user.id)


@apiv1.post("/add-bookmark", response=BookmarkOut , auth = apiAuth)
def add_bookmark(request, payload: BookmarkIn):
    # user = User.objects.get(id = request.user.id)
    course = Course.objects.get(id=payload.course_id)
    content = CourseContent.objects.get(id = payload.content_id)
    user = User.objects.get(id = request.user.id)
    bookmark = Bookmark.objects.create(
        user = user,
        course=course,
        content=content
    )
    return bookmark

@apiv1.delete("/delete-bookmark/{bookmark_id}" , auth = apiAuth)
def delete_bookmark(request, bookmark_id: int):
    user = User.objects.get(id = request.user.id)
    bookmark = Bookmark.objects.get(id=bookmark_id, user=user)
    # try:
    # except Bookmark.DoesNotExist:
    #     raise HttpError(404, "Bookmark not found")

    bookmark.delete()
    return {"success": True, "message": "Bookmark removed"}

@apiv1.put("/update-bookmark/{bookmark_id}", response=BookmarkOut , auth = apiAuth)
def edit_bookmark(request, bookmark_id: int, payload: BookmarkIn):
    bookmark = Bookmark.objects.get(id=bookmark_id, user=request.user)
    course = Course.objects.get(id=payload.course_id)
    content = CourseContent.objects.get(id=payload.content_id)
    bookmark.course = course
    bookmark.content = content
    bookmark.save()
    return bookmark

# Announcment
@apiv1.get("/announcement", response=List[AnnouncementOut] , auth = apiAuth)
def show_announcements(request, course_id: int):
    return Announcement.objects.filter(course_id=course_id)


@apiv1.post("/add-announcement", response=AnnouncementOut , auth = apiAuth)
def create_announcement(request, payload: AnnouncementIn):
    # ⚠️ Optional: validasi role teacher dulu kalau sudah ada sistem auth
    announcement = Announcement.objects.create(
        course_id=payload.course_id,
        title=payload.title,
        content=payload.content,
        publish_date=payload.publish_date
    )
    return announcement

@apiv1.put("/update-announcement/{announcement_id}", response=AnnouncementOut , auth = apiAuth)
def edit_announcement(request, announcement_id: int, payload: AnnouncementIn):
    announcement = Announcement.objects.get(id=announcement_id)
    course = Course.objects.get(id=payload.course_id)

    announcement.course = course
    announcement.title = payload.title
    announcement.content = payload.content
    announcement.publish_date = payload.publish_date
    announcement.save()

    return announcement

@apiv1.delete("/delete-announcement/{announcement_id}" , auth = apiAuth)
def delete_announcement(request, announcement_id: int):
    announcement = Announcement.objects.get(id=announcement_id)
    announcement.delete()
    return {"success": True, "message": "Announcement deleted"}

# Category
@apiv1.get("/category", response=List[CategoryOut] , auth = apiAuth)
def list_categories(request):
    return Category.objects.all()

@apiv1.post("/add-category", response=CategoryOut , auth = apiAuth)
def add_category(request, payload: CategoryIn):
    user = User.objects.get(id = request.user.id)

    category = Category.objects.create(
        name=payload.name,
        creator=user
    )
    return category

@apiv1.delete("/delete-category/{category_id}" , auth = apiAuth)
def delete_category(request, category_id: int):
    category = Category.objects.get(id=category_id)

    category.delete()
    return {"success": True, "message": "Category deleted"}
