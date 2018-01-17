import time
import lib.getconfig
import logging.handlers


log_file = lib.getconfig.getparam('daemon', 'log_file')
backupcount = int(lib.getconfig.getparam('daemon', 'log_rotate_seconds'))
seconds = int(lib.getconfig.getparam('daemon', 'log_rotate_backups'))

log = logging.handlers.TimedRotatingFileHandler(log_file, 's', seconds, backupCount=backupcount)
log.setLevel(logging.INFO)
logger = logging.getLogger('main')
logger.addHandler(log)
logger.setLevel(logging.INFO)
logger.propagate = False


def print_message(message):
    mssg = str(time.strftime("[%F %H %M:%S] ")) + message
    logger.info(mssg)

