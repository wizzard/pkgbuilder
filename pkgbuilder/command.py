from __future__ import print_function
import subprocess
import logging
import os
from pkgbuilder.conf import conf

def command_exec(cmd, ignore_error):
    logger = logging.getLogger(__name__)
    logger.debug("Executing: %s", ' '.join(cmd))
    if conf.pretend:
        return
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
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
