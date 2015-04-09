import os
from celery import Celery

app = Celery()

# Celery config
app.conf.update(BROKER_URL=os.environ.get('REDISTOGO_URL', 'redis://localhost:6379/0'),
                CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL', 'redis://localhost:6379/0'),
				CELERY_TASK_SERIALIZER='json'
				)


@app.task
def hello(filename):
	f = open(filename, 'w')
	f.write('hello, world')
	f.close()