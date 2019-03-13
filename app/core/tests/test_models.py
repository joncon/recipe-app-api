from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

''' run with

docker-compose run app sh -c "python manage.py test && flake8" '''


def sample_user(email='test@uw.edu', password='somepass'):
    '''create a sample user'''

    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email success"""
        email = 'test@email.com'
        password = 'test'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@DSAFDFD.CoM"
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creeating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@someuser.com',
            'testafsdsd'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        '''test the tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)
