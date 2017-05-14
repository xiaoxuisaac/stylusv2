"""
Custom signals sent during the registration and activation processes.

"""

from django.dispatch import Signal


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

retrieved_from_history = Signal(providing_args=["session_variable", "request","duplicate","typ"])
