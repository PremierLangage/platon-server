from datetime import timedelta
from typing import Any, Dict, Iterable, Set, Union

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible



@deconstructible
class MinDurationValidator:
    """Ensure that a DurationField is not shorter than the given duration."""
    
    
    def __init__(self, duration: Union[int, timedelta]):
        self.duration = duration.total_seconds() if isinstance(duration, timedelta) else duration
    
    
    def __call__(self, value):
        seconds = value.total_seconds() if isinstance(value, timedelta) else value
        if seconds < self.duration:
            raise ValidationError(
                'Given duration (%(value)s should not be shorter than %(duration)s',
                params={'value': value, 'duration': self.duration},
            )
    
    
    def __eq__(self, other) -> bool:
        return self.duration == other.duration


    def __ne__(self, other) -> bool:
        return self.duration != other.duration



@deconstructible
class MaxDurationValidator:
    """Ensure that a DurationField is not longer than the given duration."""
    
    
    def __init__(self, duration: Union[int, timedelta]):
        self.duration = duration.total_seconds() if isinstance(duration, timedelta) else duration
    
    
    def __call__(self, value):
        seconds = value.total_seconds() if isinstance(value, timedelta) else value
        if seconds > self.duration:
            raise ValidationError(
                'Given duration (%(value)s should not be longer than %(duration)s',
                params={'value': value, 'duration': self.duration},
            )
    
    
    def __eq__(self, other) -> bool:
        return self.duration == other.duration


    def __ne__(self, other) -> bool:
        return self.duration != other.duration



def check_unknown_fields(expected: Set[str], got: Union[Iterable[str], Dict[str, Any]]):
    """Check that every element (or key) in `got` is in `expected`.
    
    Raise `ValidationError` if any element (or key) is not in `expected`."""
    keys = set(got.keys() if isinstance(got, dict) else got)
    if unknown := (keys - expected):
        errors = {f: ["Unknown field"] for f in unknown}
        raise ValidationError(errors)



def check_unknown_missing_fields(expected: Set[str], got: Union[Iterable[str], Dict[str, Any]]):
    """Check that every element (or key) in `got` is in `expected` and that
    every element in `expected` is in (or a key of) `got`.
    
    Raise `ValidationError` if any element (or key) is not in `expected`."""
    
    keys = set(got.keys() if isinstance(got, dict) else got)
    
    errors = dict()
    if unknown := (keys - expected):
        errors = {
            **errors,
            **{f: ["Unknown field"] for f in unknown}
        }
    if missing := (expected - keys):
        errors = {
            **errors,
            **{f: ["Missing field"] for f in missing}
        }
    
    if errors:
        raise ValidationError(errors)
