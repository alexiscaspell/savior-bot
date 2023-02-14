import logging

from src.utils.file_util import make_directory_if_not_exists

_DIRECTORIO_LOGS = "logs/"
_NOMBRE_LOG_PREDEFINIDO = "savior"
_NIVEL_LOGS = "INFO"

_loggers = {}


def get_logger(nombre=_NOMBRE_LOG_PREDEFINIDO) -> logging.Logger:
    '''
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    '''

    if nombre in _loggers:
        return _loggers[nombre]

    logger = logging.getLogger(nombre)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    make_directory_if_not_exists(_DIRECTORIO_LOGS)

    logger.setLevel(_NIVEL_LOGS)

    ch = logging.StreamHandler()
    ch.setLevel(_NIVEL_LOGS)
    ch.setFormatter(formatter)

    fh = logging.FileHandler(f"{_DIRECTORIO_LOGS}/{nombre}.log")

    # fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    _loggers[nombre] = logger

    return logger

