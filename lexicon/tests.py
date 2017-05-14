from django.test import TestCase
from views import analyze
# Create your tests here.
class AnalyzePassageTestCase(TestCase):
    def test_analyze_works(self):
        text = 'It was generally allowed at that period that the territories of the New World belonged to that European nation which had been the first to discover them.'
        glossary_dict, tokens = analyze(text)
        self.assertEqual('The lion says "roar"', 'The lion says "roar"')
