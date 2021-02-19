from django.dispatch import  Signal

connect_from_lti = Signal(providing_args=["request"])
