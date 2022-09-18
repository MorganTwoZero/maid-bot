import logging.config


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'logfile': {  # The handler name
            'formatter': 'default_formatter',  # Refer to the formatter defined above
            'class': 'logging.handlers.RotatingFileHandler',  # OUTPUT: Which class to use
            'filename': 'discord.log',  # Param for class above. Defines filename to use, load it from constant
            'backupCount': 2,  # Param for class above. Defines how many log files to keep as it grows
        },
    },
    'loggers': {
        'root': {
            'handlers': ['stream_handler', 'logfile'],
            'level': 'INFO',
            'propagate': True
        },
        'main': {
            'handlers': ['stream_handler', 'logfile'],
            'level': 'INFO',
            'propagate': True
        },
        'cleaning_cog': {
            'handlers': ['stream_handler', 'logfile'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

config = logging.config.dictConfig(LOGGING_CONFIG)