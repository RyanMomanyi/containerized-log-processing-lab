import json
import os
import time
import logging
from pathlib import Path
from app.common import validate
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
SOURCE=Path(os.getenv('LOG_FILE','/data/application.jsonl'))
QUEUE=Path(os.getenv('QUEUE_DIR','/data/queue'))
POLL=float(os.getenv('POLL_SECONDS','2'))

def ingest_once(offset=0):
    QUEUE.mkdir(parents=True,exist_ok=True)
    if not SOURCE.exists():
        logging.warning('Waiting for %s',SOURCE)
        return offset,0,0
    good=bad=0
    with SOURCE.open(encoding='utf-8') as inp:
        inp.seek(offset)
        while True:
            line=inp.readline()
            if not line:
                break
            if not line.strip(): continue
            record,error=validate(line)
            if error:
                bad+=1;logging.warning('Rejected malformed record: %s',error)
                continue
            import uuid
            dest=QUEUE / (str(uuid.uuid4())+'.json')
            dest.write_text(json.dumps(record),encoding='utf-8')
            good+=1
        offset=inp.tell()
    return offset,good,bad

if __name__=='__main__':
    offset=0
    while True:
        if SOURCE.exists() and SOURCE.stat().st_size < offset:
            offset=0
        offset,good,bad=ingest_once(offset)
        if good or bad:logging.info('Enqueued %d; rejected %d',good,bad)
        time.sleep(POLL)
