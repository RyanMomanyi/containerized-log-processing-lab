import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
file=Path(os.getenv('LOG_FILE','./data/application.jsonl'))
file.parent.mkdir(parents=True,exist_ok=True)
count=int(sys.argv[1]) if len(sys.argv)>1 else 20
random.seed(42)
with file.open('a',encoding='utf-8') as f:
    for i in range(count):
        row={'timestamp':datetime.now(timezone.utc).isoformat(),'service':random.choice(['api','web','auth']), 'level':random.choice(['INFO','INFO','WARNING','ERROR']),'message':f'synthetic event {i}'}
        f.write(json.dumps(row)+'\n')
print(f'Wrote {count} synthetic records to {file}')
