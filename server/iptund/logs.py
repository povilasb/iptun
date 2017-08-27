import logging


def setup(config: dict) -> None:
    """Setup logging to file.

    Args:
        config: ['level'] - logging level: 'INFO', 'WARNING', etc.
                ['file'] - writes logs to this file. E.g. '/tmp/myapp.log'.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.__dict__[config['level']])
    handler = logging.FileHandler(config['file'])
    handler.setFormatter(logging.Formatter(
        '$asctime $levelname $filename:$lineno $message',
        style='$',
    ))
    logger.addHandler(handler)
