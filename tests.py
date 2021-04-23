from unittest import TestCase

import app, find_id
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

Session = sessionmaker()


# class MyTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = create_engine('sqlite:///:memory:')
#         self.connection = self.engine.connect()
#         self.trans = self.connection.begin()
#         self.session = Session(bind=self.connection)
#
#
#     def test_search(self):
#         pass


class TestFindIDTeacher(TestCase):
    def test_find_id_teacher1(self):
        self.assertEqual(find_id.find_id_teacher('Noyce'), 1)

    def test_find_id_teacher2(self):
        self.assertEqual(find_id.find_id_teacher('Dles'), 5)

    def test_find_id_teacher3(self):
        self.assertRaises(TypeError, find_id.find_id_teacher, 3)


class TestFindIDRoom(TestCase):
    def test_find_id_room1(self):
        self.assertEqual(find_id.find_id_room('CB5'), 1)

    def test_find_id_room2(self):
        self.assertEqual(find_id.find_id_room('sBr5'), 2)

    def test_find_id_room3(self):
        self.assertRaises(TypeError, find_id.find_id_room, 3)


class TestFindIDActivity(TestCase):

    def test_find_id_activity1(self):
        self.assertEqual(find_id.find_id_activity('Chess'), 1)

    def test_find_id_activity2(self):
        self.assertEqual(find_id.find_id_activity('Mahs'), 4)

    def test_find_id_activity3(self):
        self.assertRaises(TypeError, find_id.find_id_activity, 3)


class TestIntersection(TestCase):
    def test_intersection1(self):
        self.assertEqual(app.intersection([1, 2, 3, 4, 5], [2, 3, 4, 5, 6, 7], [4, 5, 6, 7, 8]), [4, 5])

    def test_intersection2(self):
        self.assertEqual(app.intersection([1, 2, 3, 4, 5], [2, 3, 4, 5, 6, 7], [4, 5, 6, 7, 8], []), [4, 5])

    def test_intersection3(self):
        self.assertNotEqual(app.intersection([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]), [1, 2, 3, 4, 5, 6])

    def test_intersection4(self):
        self.assertRaises(TypeError, app.intersection, 1, 2, 3)
