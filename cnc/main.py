#!/usr/bin/env python

import os
import sys
import readline
import atexit
import BaseHTTPServer

import cnc.logging_config as logging_config
from cnc.gcode import GCode, GCodeException
from cnc.gmachine import GMachine, GMachineException

class SimpleRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):

        print self.path
        self.wfile.write('HTTP-1.0 200 Okay\r\n\r\nHere is your output for '+self.path)

    def do_POST(self):

        print self.path
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        self.wfile.write('HTTP-1.0 200 Okay\r\n\r\n' + post_data)
        do_line(post_data)

def run(server_class=BaseHTTPServer.HTTPServer,
    handler_class=SimpleRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

try:  # python3 compatibility
    type(raw_input)
except NameError:
    # noinspection PyShadowingBuiltins
    raw_input = input

# configure history file for interactive mode
history_file = os.path.join(os.environ['HOME'], '.pycnc_history')
try:
    readline.read_history_file(history_file)
except IOError:
    pass
readline.set_history_length(1000)
atexit.register(readline.write_history_file, history_file)

machine = GMachine()


def do_line(line):
    try:
        g = GCode.parse_line(line)
        res = machine.do_command(g)
    except (GCodeException, GMachineException) as e:
        print('ERROR ' + str(e))
        return False
    if res is not None:
        print('OK ' + res)
    else:
        print('OK')
    return True


def main():
    logging_config.debug_disable()
    try:
        if len(sys.argv) > 1:
            print("**************" + sys.argv[1])
            if sys.argv[1] == "api":
                print("listen on port 8000")
                run()
            else:
            # Read file with gcode
                with open(sys.argv[1], 'r') as f:
                    for line in f:
                        line = line.strip()
                        print('> ' + line)
                        if not do_line(line):
                            break
        else:
            # Main loop for interactive shell
            # Use stdin/stdout, additional interfaces like
            # UART, Socket or any other can be added.
            print("*************** Welcome to PyCNC!!!! ***************")
            while True:
                line = raw_input('> ')
                if line == 'quit' or line == 'exit':
                    break
                do_line(line)
    except KeyboardInterrupt:
        pass
    print("\r\nExiting...")
    machine.release()


# if __name__ == "__main__":
#     main()
