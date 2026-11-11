import unittest
import json
from app.common import validate
class ValidationTests(unittest.TestCase):
    def test_valid(self):
        obj={'timestamp':'2026-11-10T12:00:00Z','service':'api','level':'ERROR','message':'timeout'}
        self.assertIsNone(validate(json.dumps(obj))[1])
    def test_bad_json(self):
        self.assertIsNotNone(validate('{bad')[1])
    def test_missing_field(self):
        self.assertIsNotNone(validate('{"service":"api"}')[1])
    def test_bad_level(self):
        obj={'timestamp':'2026-11-10T12:00:00Z','service':'api','level':'FATAL','message':'x'}
        self.assertIsNotNone(validate(json.dumps(obj))[1])
if __name__=='__main__':unittest.main()
