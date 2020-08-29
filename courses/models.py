from django.db import models
from django.urls import reverse

from memberships.models import Membership


class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    #allowed memberships is a many to many field as we'll allow
    #many memberships most likely
    allowed_memberships = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    #this is a convinience method on course model
    def get_absolute_url(self):
        #namespace for the url is courses and detail is the url where we want to go from that namespace
        #we only need slug as the only parameter because slug was the only thing passed in urls.py for courseDetailView
        #we pass self.slug as slug is a field on course
        return reverse('courses:detail', kwargs={'slug': self.slug})

    @property
    def lessons(self):
        #here after self . we grab the course object lesson
        #lesson is grabbed from Lesson method below so if Lesson class was called lecture
        #we'd grab it as set.lecture_set.all()

        #lessons are ordered by position (grabbed from Lesson class) so that they may appear in
        #an order and not randomly
        return self.lesson_set.all().order_by('position')
        #lesson set is the syntax for Foreign key object


class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    #as we pass courses as foreign key inside lessons
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson-detail',
        kwargs={ 
            'course_slug': self.course.slug,
            'lesson_slug': self.slug
        })
