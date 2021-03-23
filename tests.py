from unittest import TestCase

import app
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_teachers(self):
        result = self.app.get('/')
        # Make your assertions


class TestFindID(TestCase):
    def test_find_id_teacher(self):
        self.assertEqual(1, 1)

    def test_find_id_room(self):
        self.fail()

    def test_find_id_activity(self):
        self.fail()
