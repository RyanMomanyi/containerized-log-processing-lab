import json
import os
import time
import logging
from pathlib import Path
import psycopg
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
QUEUE=Path(os.getenv('QUEUE_DIR','/data/queue'))
POLL=float(os.getenv('POLL_SECONDS','2'))
DSN=os.getenv('DATABASE_URL','postgresql://lab:lab@db:5432/logs')
SQL='CREATE TABLE IF NOT EXISTS app_logs (id BIGSERIAL PRIMARY KEY, event_time TIMESTAMPTZ NOT NULL, service TEXT NOT NULL, level TEXT NOT NULL, message TEXT NOT NULL)'

def process_once():
    QUEUE.mkdir(parents=True,exist_ok=True)
    with psycopg.connect(DSN) as conn:
        conn.execute(SQL)
        processed=0
        for item in sorted(QUEUE.glob('*.json')):
            try:
                obj=json.loads(item.read_text(encoding='utf-8'))
                with conn.transaction():
                    conn.execute('INSERT INTO app_logs (event_time,service,level,message) VALUES (%s,%s,%s,%s)',(obj['timestamp'],obj['service'],obj['level'],obj['message']))
                item.unlink()
                processed+=1
            except Exception:
                logging.exception('Could not process %s; leaving for retry', item)
        return processed

if __name__=='__main__':
    while True:
        try:
            n=process_once()
            if n: logging.info('Stored %d records',n)
        except psycopg.OperationalError:
            logging.exception('Database unavailable; retrying')
        time.sleep(POLL)
