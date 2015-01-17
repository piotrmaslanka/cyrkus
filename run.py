import sys
from satella.unix import daemonize

from cyrkus.reporter.run import run as run_reporter
from cyrkus.shared.config import get_conf

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Expected only one argument - "reporter" or "redaction"')
        sys.exit()

    conf = get_conf()

    daemonize()

    if sys.argv[1] == 'reporter':
        run_reporter(conf)
    elif sys.argv[1] == 'redaction':
        from cyrkus.redaction.run import run
        run(conf)
