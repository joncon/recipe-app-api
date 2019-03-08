from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTests(TestCase):
    '''Test the users api (public)'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        '''Test user with valid payload is successful '''
        payload = {
            'email': 'student@uw.edu',
            'password': 'somepass',
            'name': 'name goes here'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        '''test creating existing user fails'''

        payload = {
            'email': 'sucha-unique@uw.edu',
            'password': 'somepass',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short(self):
        '''password must be more than 5 chars'''

        payload = {
            'email': 'studen@uw.edu',
            'password': 'pw',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def create_token_for_user(self):
        '''test that a token is created for user'''

        payload = {'email': 'test@uw.edu', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_creations(self):
        '''token is not created if invalid token given'''

        create_user(email='test@uw.edu', password='testpass')
        payload = {'email': 'test@uw.edu', 'password': 'wrong '}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''test that token is not created if user doesnt exist'''
        payload = {'email': 'test@uw.edu', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''test that email and password are required'''
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        '''auth required for users'''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivateUserApiTests(TestCase):
#     '''Test API requests that require authentication'''
#
#     def setUp(self):
#         self.user = create_user(
#             email='test@uw.edu',
#             password='testpasss',
#             name='name'
#         )
#
#         self.client = APIClient()
#         # force_authenticate is a helper method to bypass authenication
#         self.client.force_authenticate(user=self.user)
#
#     def test_test_retrieve_profile_success(self):
#         '''test retrieving profile for logged in user'''
#
#         res = self.client.get(ME_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {
#             'name': self.user.name,
#             'email': self.user.password
#         })
#
#     def test_post_me_not_allowed(self):
#         '''test that post is not allowed on the me url'''
#         res = self.client.post(ME_URL, {})
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_update_user_profile(self):
#         '''test updating uthe user profile for authenticated user'''
#
#         payload = {'name': 'new_name', 'password': 'newpassws'}
#         res = self.client.patch(ME_URL, payload)
#
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.name, payload['name'])
#         self.assertTrue(self.user.check_password(payload['password']))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
