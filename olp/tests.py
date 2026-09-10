from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from olp.models import Enrollment, Order, Profile, Role


class AuthFlowTests(TestCase):
    def test_register_creates_profile_and_student_role(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'learner1',
                'first_name': 'Learn',
                'last_name': 'Er',
                'email': 'learner@example.com',
                'phone': '1234567890',
                'field': 'CS',
                'password1': 'ComplexPass123!',
                'password2': 'ComplexPass123!',
            },
        )
        self.assertRedirects(response, reverse('profile'))
        user = get_user_model().objects.get(username='learner1')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertTrue(user.profile.roles.filter(name='student').exists())

    def test_logout_requires_post(self):
        user = get_user_model().objects.create_user(username='u1', password='ComplexPass123!')
        Profile.objects.create(user=user, phone='1', field='x')
        self.client.login(username='u1', password='ComplexPass123!')

        get_response = self.client.get(reverse('logout'))
        self.assertRedirects(get_response, reverse('home'))
        self.assertTrue(get_user_model().objects.filter(username='u1').exists())
        # GET must not log the user out
        self.assertTrue('_auth_user_id' in self.client.session)

        post_response = self.client.post(reverse('logout'))
        self.assertRedirects(post_response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)


class ModelConstraintTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='student', password='ComplexPass123!')
        self.instructor = User.objects.create_user(username='teacher', password='ComplexPass123!')
        from olp.models import Course

        self.course = Course.objects.create(
            title='Django 101',
            description='Intro',
            instructor=self.instructor,
            price='10.00',
        )

    def test_enrollment_unique_per_user_course(self):
        Enrollment.objects.create(user=self.user, course=self.course)
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(user=self.user, course=self.course)

    def test_order_has_required_relations(self):
        order = Order.objects.create(
            user=self.user,
            course=self.course,
            transaction_id='txn-1',
        )
        self.assertEqual(order.status, 'PENDING')
        self.assertEqual(str(order.course), 'Django 101')


class RoleModelTests(TestCase):
    def test_role_permissions_m2m(self):
        from olp.models import Permission

        role = Role.objects.create(name='instructor')
        permission = Permission.objects.create(name='edit_course')
        role.permissions.add(permission)
        self.assertEqual(role.permissions.count(), 1)
