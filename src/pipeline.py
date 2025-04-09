import os
import sys

class Pipeline:
    curr_status_code = 0

    def execute(self, commands):
        if len(commands) == 1:
            return commands[0].run(sys.stdin, sys.stdout, sys.stderr)
        else:
            read_d = None
            write_d = None
            r = None

            in_pipe = sys.stdin
            out_pipe = sys.stdout
            err_pipe = sys.stderr

            for i, cmd in enumerate(commands):
                if i == 0:
                    r, write_d = os.pipe()
                    in_pipe = sys.stdin
                    r = os.fdopen(r, 'r')
                    out_pipe = os.fdopen(write_d, 'w') 
                elif i == len(commands) - 1:
                    in_pipe = read_d
                    out_pipe = sys.stdout
                else:
                    r, write_d = os.pipe()
                    r = os.fdopen(r, 'r')
                    in_pipe = read_d
                    out_pipe = os.fdopen(write_d, 'w') 

                curr_status_code = cmd.run(in_pipe, out_pipe, err_pipe)
                read_d = r
                # os.close(in_pipe_.fileno())
                # os.close(out_pipe_.fileno())
                if i != len(commands) - 1:
                    out_pipe.close()

            return curr_status_code
            

