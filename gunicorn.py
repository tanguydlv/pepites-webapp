import multiprocessing
import gunicorn

gunicorn.SERVER_SOFTWARE = 'NOP'

bind = '0.0.0.0:8080'

worker_class = 'eventlet'
workers = multiprocessing.cpu_count() * 2 + 1

accesslog = '-'
errorlog = '-'
loglevel = 'info'
capture_output = True
timeout = 120
