from functools import wraps
import logging
import time

log = logging.getLogger('s3_backups')

# Define colors for the ColoredFormatter
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
COLORS = {
    'WARNING': CYAN,
    'INFO': WHITE,
    'DEBUG': GREEN,
    'CRITICAL': RED,
    'ERROR': RED
}
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        color = COLOR_SEQ % (30 + COLORS[levelname])
        message = logging.Formatter.format(self, record)
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ).replace("$COLOR", color)
        for k, v in COLORS.items():
            message = message.replace("$" + k, COLOR_SEQ % (v + 30)).replace("$BG" + k, COLOR_SEQ % (v + 40)).replace("$BG-" + k, COLOR_SEQ % (v + 40))
        return message + RESET_SEQ


def timeit(message="%(func_name)r (%(args)r, %(kwargs)r) %(time)s"):
    def _timeit(func):
        def _decorator(*args, **kwargs):
            ts = time.time()
            result = func(*args, **kwargs)
            te = time.time()
            elapsed = te - ts
            time_str = "%2.2f seconds" % elapsed
            if elapsed > 60:
                time_str = "%2.2f minutes" % (elapsed / 60)
            log.info(message % {'time': time_str, 'func_name': func.__name__, 'args': args, 'kwargs': kwargs})
            return result
        return wraps(func)(_decorator)
    return _timeit
