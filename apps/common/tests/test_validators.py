from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from common import validators



class MaxDurationValidatorTestCase(TestCase):
    
    def test_call_int(self):
        validator = validators.MaxDurationValidator(100)
        
        # Should work
        validator(10)
        validator(timedelta(minutes=1))
        
        with self.assertRaises(ValidationError):
            validator(101)
        with self.assertRaises(ValidationError):
            validator(timedelta(minutes=2))
    
    
    def test_call_timedelta(self):
        validator = validators.MaxDurationValidator(timedelta(minutes=2))
        
        # Should work
        validator(10)
        validator(timedelta(minutes=1))
        
        with self.assertRaises(ValidationError):
            validator(200)
        with self.assertRaises(ValidationError):
            validator(timedelta(minutes=3))
    
    
    def test_equal(self):
        self.assertEqual(
            validators.MaxDurationValidator(100),
            validators.MaxDurationValidator(100)
        )
        self.assertNotEqual(
            validators.MaxDurationValidator(100),
            validators.MaxDurationValidator(200)
        )



class MinDurationValidatorTestCase(TestCase):
    
    def test_call_int(self):
        validator = validators.MinDurationValidator(120)
        
        # Should work
        validator(130)
        validator(timedelta(minutes=2))
        
        with self.assertRaises(ValidationError):
            validator(100)
        with self.assertRaises(ValidationError):
            validator(timedelta(minutes=1))
    
    
    def test_call_timedelta(self):
        validator = validators.MinDurationValidator(timedelta(minutes=2))
        
        # Should work
        validator(120)
        validator(timedelta(minutes=3))
        
        with self.assertRaises(ValidationError):
            validator(60)
        with self.assertRaises(ValidationError):
            validator(timedelta(minutes=1))
    
    
    def test_equal(self):
        self.assertEqual(
            validators.MinDurationValidator(100),
            validators.MinDurationValidator(100)
        )
        self.assertNotEqual(
            validators.MinDurationValidator(100),
            validators.MinDurationValidator(200)
        )



class CheckUnknownFieldsTestCase(TestCase):
    
    def test_ok_iter(self):
        expected = {"field1", "field2", "field3"}
        ok1 = {"field1"}
        ok2 = {"field3", "field2"}
        wrong1 = {"field1", "unknown"}
        wrong2 = {"unknown"}
        
        # Should work
        validators.check_unknown_fields(expected, ok1)
        validators.check_unknown_fields(expected, ok2)
        
        with self.assertRaises(ValidationError):
            validators.check_unknown_fields(expected, wrong1)
        with self.assertRaises(ValidationError):
            validators.check_unknown_fields(expected, wrong2)
    
    
    def test_ok_dict(self):
        expected = {"field1", "field2", "field3"}
        ok1 = {"field1": 1}
        ok2 = {"field3": 1, "field2": 1}
        wrong1 = {"field1": 1, "unknown": 1}
        wrong2 = {"unknown": 1}
        
        # Should work
        validators.check_unknown_fields(expected, ok1)
        validators.check_unknown_fields(expected, ok2)
        
        with self.assertRaises(ValidationError):
            validators.check_unknown_fields(expected, wrong1)
        with self.assertRaises(ValidationError):
            validators.check_unknown_fields(expected, wrong2)



class CheckUnknownMissingFieldsTestCase(TestCase):
    
    def test_ok_iter(self):
        expected = {"field1", "field2", "field3"}
        ok = {"field1", "field2", "field3"}
        missing = {"field1", "field2"}
        unknown = {"field1", "field2", "field3", "unknown"}
        missing_unknown = {"field1", "field2", "unknown"}
        
        # Should work
        validators.check_unknown_missing_fields(expected, ok)
        
        with self.assertRaises(ValidationError):
            validators.check_unknown_missing_fields(expected, missing)
        with self.assertRaises(ValidationError):
            validators.check_unknown_missing_fields(expected, unknown)
        with self.assertRaises(ValidationError):
            validators.check_unknown_missing_fields(expected, missing_unknown)
    
    
    def test_ok_dict(self):
        expected = {"field1", "field2", "field3"}
        ok = {"field1": 1, "field2": 1, "field3": 1}
        missing = {"field1": 1, "field2": 1}
        unknown = {"field1": 1, "field2": 1, "field3": 1, "unknown": 1}
        missing_unknown = {"field1": 1, "field2": 1, "unknown": 1}
        
        # Should work
        validators.check_unknown_missing_fields(expected, ok)
        
        with self.assertRaises(ValidationError):
            validators.check_unknown_missing_fields(expected, missing)
        with self.assertRaises(ValidationError):
            validators.check_unknown_missing_fields(expected, unknown)
        with self.assertRaises(ValidationError):
            validators.check_unknown_missing_fields(expected, missing_unknown)
