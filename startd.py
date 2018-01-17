import os
import sys
from lib.daemon import daemon
import lib.pushdata
import lib.getconfig
import lib.daemonlog


sys.path.append(os.path.dirname(os.path.realpath("__file__"))+'/lib')

pidfile = lib.getconfig.getparam('daemon', 'pid_file')
workers = int(lib.getconfig.getparam('daemon', 'threads'))


class App(daemon):
    def run(self):
        try:
            lib.pushdata.runworker(workers)
            lib.daemonlog.print_message('Starting ' + str(workers) + ' consumer threads')
        except Exception as err:
            lib.daemonlog.print_message(str(err))


if __name__ == "__main__":
        daemon = App(pidfile)
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    daemon.start()
            elif 'stop' == sys.argv[1]:
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    daemon.restart()
            else:
                    print ("Unknown command")
                    sys.exit(2)
            sys.exit(0)
        else:
            print(("usage: %s start|stop|restart" % sys.argv[0]))
            sys.exit(2)







