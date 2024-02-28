from loguru import logger


def setup_logging(app_root):
    log_file_path = app_root / "logs/application.log"
    logger.add(log_file_path, rotation="50 MB")
