import os
import logging

if os.getenv("DEBUG") == 'TRUE':
    logging.basicConfig(level=logging.DEBUG)
else:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'TRUE'
