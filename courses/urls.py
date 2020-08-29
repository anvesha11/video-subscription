from django.urls import path
from .views import CourseListView, CourseDetailView, LessonDetailView

app_name = 'courses'

urlpatterns = [
    #we don't wanna have a path to admin here so put an empty string
    path('', CourseListView.as_view(), name='list'),
    path('<slug>', CourseDetailView.as_view(), name='detail'),
    path('<course_slug>/<lesson_slug>', LessonDetailView.as_view(), name='lesson-detail')
]