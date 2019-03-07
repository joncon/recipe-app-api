from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        '''Test waiting for db'''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            # call count is mock method
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    # the ts arg is passed in from the decorator (time.sleep)
    def test_wait_for_db(self, ts):
        '''Test waiting for db'''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # this will raise error first 5 times then on 6th, no error
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
