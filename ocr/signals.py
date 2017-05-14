"""
Custom signals sent during the registration and activation processes.

"""

from django.dispatch import Signal


# A new user has registered.
file_ocred = Signal(providing_args=[ "request",'name', 'pages', 'url'])
