from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView, View
#detail view gives a more detailed description of every view
from memberships.models import UserMembership
from .models import Course, Lesson
#using class based views as it's esentially the simplest way to do it

#CourseListView is inherited from ListView so it takes it as a parameter
class CourseListView(ListView):
    model = Course
class CourseDetailView(DetailView):
    model = Course

class LessonDetailView(View):
    #we filter courses and lessons using slugs
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        # course_qs = Course.objects.filter(slug=course_slug)
        # # if course_qs.exists():
        # course = course_qs.first()
        #qs is query set 
        #how do we actually get lessons to filter out?
        #lessons are grabbed from the models.py we just edited
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        
        #check the type of membership first & based on that, we'll decide what to show to the user
        user_membership = UserMembership.objects.filter(user=request.user).first()

        #here .membership signifies that to grab the membership type we visit class Membership and
        #the second .membership_type says that it's a variable field in the class Membership
        user_membership_type = user_membership.membership.membership_type

        #now we grab the courses associated with this membership type only
        #for this we use objects associated with Course method
        #we take .all() as it is a many to many field
        course_allowed_mem_types = course.allowed_memberships.all()


        context = {
            'object': None
        }

        #initially context is set to NULL, because it's later that we're gonna display videos based on
        #the type of membership the user has chosen

        #if membership_type (gotten from Membership class) is equal to user_membership_type grabbed from above
        #meaning, the user should have entered a valid membership type
        if course_allowed_mem_types.filter(membership_type = user_membership_type).exists():
            context = {'object': lesson}




        return render(request, "courses/lesson_detail.html", context)