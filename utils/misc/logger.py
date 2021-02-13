# -*- coding: utf-8 -*-

import logging


logging.basicConfig(
    level=logging.INFO,
    filename='logs/logger.log',
    format='%(asctime)s | %(name)s | %(levelname)-4s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

logger = logging.getLogger()
