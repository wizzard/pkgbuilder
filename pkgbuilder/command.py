from __future__ import print_function
import subprocess
import logging
from pkgbuilder.conf import conf


def command_exec(cmd, ignore_error=False):
    logger = logging.getLogger(__name__)
    logger.debug("Executing: %s", ' '.join(cmd))
    if conf.pretend:
        return None
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()

    except subprocess.CalledProcessError as e:
        logger.debug("Error: %s", e.output)
        if ignore_error:
            pass
        else:
            raise
    except OSError as e:
        if ignore_error:
            pass
        else:
            raise
