import os
import json
from datetime import datetime, timezone
REQUIRED = {'timestamp','service','level','message'}
LEVELS = {'DEBUG','INFO','WARNING','ERROR','CRITICAL'}

def validate(line):
    try:
        obj=json.loads(line)
        if not isinstance(obj,dict) or not REQUIRED.issubset(obj):
            return None, 'missing required fields'
        if not all(isinstance(obj[k],str) and obj[k].strip() for k in REQUIRED):
            return None, 'required fields must be nonempty strings'
        if obj['level'] not in LEVELS:
            return None, 'invalid level'
        datetime.fromisoformat(obj['timestamp'].replace('Z','+00:00'))
        return obj,None
    except (ValueError,TypeError, json.JSONDecodeError):
        return None, 'invalid JSON or timestamp'
