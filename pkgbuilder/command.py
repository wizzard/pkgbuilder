from __future__ import print_function
import subprocess
import logging
from pkgbuilder.conf import conf


def command_exec(cmd, ignore_error):
    logger = logging.getLogger(__name__)
    logger.debug("Executing: %s", ' '.join(cmd))
    if conf.pretend:
        return
    try:
        # subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, b''):
            print(line)
        p.stdout.close()
        p.wait()

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
