"""
Custom signals sent during the registration and activation processes.

"""

from django.dispatch import Signal


# A new user has registered.
text_analyzed = Signal(providing_args=["session_variable", "request",'text'])
pdf_created = Signal(providing_args=["session_variable", "request"])
all_defs_got = Signal(providing_args=["session_variable", "lemmas", "request"])
defs_changed = Signal(providing_args=["session_variable", "lemmas", "request"])
quiz_created = Signal(providing_args=["session_variable", "request"])
lemma_added = Signal(providing_args=["request","tokens", "lemmas", "lemma"])


VOCAB_PDF = intern('Vocab'.encode('utf8'))
QUIZ_PDF = intern('Quiz'.encode('utf8'))
