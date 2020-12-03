## brainf code translation

### Works in Windows and Unix


def bf2py(bf):
    code = """
try: # Windows
    from msvcrt import getch
except: # Unix
    import sys, tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


stack_len = 30000
stack = [0 for i in range(stack_len)]
ptr = 0
""" 
    return code + _bf2py(bf)

def _indent(code):
    return "\n".join(["\t"+i for i in code.split("\n")])


def _bf2py(bf):
    
    code = ""
    while len(bf):
        command, bf = bf[0], bf[1:]
        if command in ["+", "-"]:
            ptrchange = eval(command+"1")
            try:
                while bf[0] in ["+", "-"]:
                    ptrchange, bf = ptrchange + eval(bf[0]+"1"), bf[1:]
            except IndexError: pass
            finally:
                code += f"stack[ptr] = (stack[ptr] + ({ptrchange})) % 256\n"

        elif command in ["<", ">"]:
            ptrchange = -1 if command == "<" else 1
            try:
                while bf[0] in ["<", ">"]:
                    ptrchange, bf = ptrchange + (-1 if bf[0] == "<" else 1), bf[1:]
            except IndexError: pass
            finally:
                code += f"ptr = (ptr + ({ptrchange})) % stack_len\n" 
        
        elif command == ".":
            code += "print(chr(stack[ptr]), end=\"\")\n"
        elif command == ",":
            code += "stack[ptr] = ord(getch())\n"
        
        elif command == "[":
            i = 0
            counter = 1
            while counter != 0:
                if bf[0] == "[": counter += 1
                elif bf[0] == "]": counter -= 1
                command, bf = command + bf[0], bf[1:]
            command = command[1:-1]
            code += """
while stack[ptr]:
""" + _indent(_bf2py(command)) + "\n"

    return code.strip()

def bf(code):
    exec(bf2py(code))



bf("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")
bf("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.")
