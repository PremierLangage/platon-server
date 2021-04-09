from django.http import Http404
from django.test import TestCase

from pl_core import enums



class ErrorCodeTestCase(TestCase):
    
    def test_from_exception(self):
        self.assertEqual(
            enums.ErrorCode.Http404,
            enums.ErrorCode.from_exception(Http404())
        )
        self.assertEqual(
            enums.ErrorCode.UNKNOWN,
            enums.ErrorCode.from_exception(Exception())
        )
