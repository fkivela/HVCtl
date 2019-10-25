"""An example about redirecting the input and print functions."""

import sys
import threading
import pty

# Slave simulates a terminal; master simulates the underlying 
# machinery.
# Slave can be written to and master can be read from.
# Vice versa doesn't work.

master1, slave1 = pty.openpty()
user_write = open(slave1, 'w')
script_read = open(master1, 'r')

master2, slave2 = pty.openpty()
script_write = open(slave2, 'w')
user_read = open(master2, 'r')

sys.stdout = script_write
sys.stdin = script_read

def script():    
    while True:
        print('Give some input: ', end='', flush=True)
        string = input()
        print(f'You gave the following input: {string}', flush=True)
                
def ui_loop():
    while True:
        prompt = user_read.read(17)
        print(prompt, file=sys.__stdout__, end='', flush=True)
        # Print only flushes if end is '\n'
        
        input_str = sys.__stdin__.readline()
        if input_str in ('q\n', 'x\n'):
            break
        user_write.write(input_str)
        
        output_str = user_read.readline()
        print(output_str, file=sys.__stdout__, end='', flush=True)
    
thread = threading.Thread(target=script, daemon=True)
thread.start()
ui_loop()