import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
logger = logging.getLogger(__name__)
