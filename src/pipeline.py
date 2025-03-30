
import os
import sys

class Pipeline:
    curr_status_code = 0

    @staticmethod
    def execute(commands):
        if len(commands) == 1:
            return cmd.run(sys.stdin, sys.stdout, sys.stderr)
        else:
            read_d = None
            write_d = None
            
            in_pipe = sys.stdin
            out_pipe = sys.stdout
            err_pipe = os.stderr

            for i, cmd in enumerate(commands):
                if i == 0:
                    read_d, write_d = os.pipe()
                    in_pipe = sys.stdin
                    out_pipe = write_d
                elif i == len(commands) - 1:
                    in_pipe = read_d
                    out_pipe = sys.stdout
                else:
                    read_d, write_d = os.pipe()
                    in_pipe = read_d
                    out_pipe = write_d

                os.close(in_pipe)
                curr_status_code = cmd.run(in_pipe, out_pipe, err_pipe)
                
            return curr_status_code
            

