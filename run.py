# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sys import exit
from apps import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = True

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

app = create_app()

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
