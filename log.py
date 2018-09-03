import logging
from logging.handlers import SMTPHandler
from logging.config import dictConfig
# 必须在 Flask(__name__)  之前加载
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
#
#
# mail_handler = SMTPHandler(
#     mailhost='127.0.0.1',
#     fromaddr='server-error@example.com',
#     toaddrs=['admin@example.com'],
#     subject='Application Error'
# )
# mail_handler.setLevel(logging.ERROR)
# mail_handler.setFormatter(logging.Formatter(
#     '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
# ))

