import os

_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'))
_VAR = os.path.join(_ROOT, 'var')
_ETC = os.path.join(_ROOT, 'etc')

loglevel = 'info'
# errorlog = os.path.join(_VAR, 'log/api-error.log')
# accesslog = os.path.join(_VAR, 'log/api-access.log')
errorlog = "-"
accesslog = "-"
# bind = 'unix:%s' % os.path.join(_VAR, 'run/gunicorn.sock')
bind = '0.0.0.0:80'

# workers = 4
# workers = multiprocessing.cpu_count() * 2 + 1
threads = 2

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True
