# coding: utf-8

from psycopg2 import IntegrityError

from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger

class GlobalTestOpenAcademyCourse(TransactionCase):
    '''
    Global test to openacademy course model.
    Test create course and trigger constraints.
    '''
    def setUp(self):
        # Define global variables to test methods
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.course = self.env['openacademy.course']
    # Method of class
    # Method of class that isn't test.
    def create_course(self,
                      course_name,
                      course_description,
                      course_responsible_id):
        # Create a course with recieved parameters
        course_id = self.course.create({
            'name': course_name,
            'description': course_description,
            'responsible_id': course_responsible_id
        })
        return course_id

    # Method of test starts with 'def test_*(self):'

    # Mute the openerp.sql_db error to avoid it in log.
    @mute_logger('openerp.sql_db')
    def test_10_same_name_description(self):
        '''
        Test to create a course with same name and description.
        To raise constraint of different name to description.
        '''
        # Expected raised error with expected message.
        with self.assertRaisesRegexp(
                IntegrityError,
                'new row for relation "openacademy_course" violates check'
                ' constraint "openacademy_course_name_description_check"'
                ):
            # Create a course with same name and description.
            self.create_course('test', 'test', None)


    @mute_logger('openerp.sql_db')
    def test_20_two_courses_same_name_description(self):
        '''
        Test to create two courses with same name.
        To raise constraint of different name to description.
        '''
        new_id = self.create_course('test1', 'test_description', None)
        with self.assertRaisesRegexp(
            IntegrityError,
            'duplicate key value violates unique '
            'constraint "openacademy_course_name_unique"'
            ):
            new_id2 = self.create_course('test1', 'test_description', None)

    def test_30_duplicate_course(self):
        '''
        Test to duplicate a course and check that works fine.
        '''
        course = self.env.ref('openacademy.course0')
        course.copy()
