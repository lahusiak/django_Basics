from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Course, Step

class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Regular Expressions",
            description="Learn to write regular expressions"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)

class StepModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write tests in Python"
        )
    def test_step_creation(self):
        step = Step.objects.create(
            title="Step 1",
            description="Take a step",
            course=self.course
        )
        self.assertIn(step, self.course.step_set.all())

class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="More Python",
            description="How cool is that!"
        )
        self.course2 = Course.objects.create(
            title="More Python 2",
            description="How cool is that 2222!"
        )
        self.step = Step.objects.create(
            title="Intro to doctests",
            description="Test driven!",
            course=self.course
        )
    def test_course_list_views(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])

    def test_course_detail_views(self):
        resp = self.client.get(reverse('courses:detail', kwargs={
            'pk': self.course.pk,
            }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])

    def test_course_step_views(self):
        resp = self.client.get(reverse('courses:step', kwargs={
            'course_pk': self.course.pk,
            'step_pk': self.step.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])

