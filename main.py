import sys, logging
from datetime import datetime

optimization_option = 0 # 0, 1, 2

def find_bracket(code, pos, bracket):
    cont = 0
    pair = '[' if bracket == ']' else ']'
    for a, i in zip(code[pos:], range(pos, len(code))):
        if a == bracket:
            cont = cont + 1
        if a == pair:
            if cont == 0:
                return i
            else:
                cont = cont - 1

    raise Exception("Could not find `{}``bracket\nPosition: {}"
                    .format(pair, pos))

def prepare_code(code):
    def map_left_bracket(b, p):
        return (b, find_bracket(code, p + 1, b))

    def map_right_bracket(b, p):
        offset = find_bracket(list(reversed(code[:p])), 0, ']')
        return (b, p - offset)

    def map_bracket(b, p):
        if b == '[':
            return map_left_bracket(b, p)
        else:
            return map_right_bracket(b, p)

    return [map_bracket(c, i) if c in ('[', ']') else c
            for c, i in zip(code, range(len(code)))]


def read(string):
    valid = ['>', '<', '+', '-', '.', ',', '[', ']']
    return prepare_code([c for c in string if c in valid])

debug_file = open("debug.log", "w")

def eval_step(code, data, code_pos, data_pos, out=sys.stdout.write):
    c = code[code_pos]
    d = data[data_pos]
    step = 1
    if c != ">":
        debug_file.write(f"another_instruction: {c}, data_pos:{data_pos}\n")
    #TODO: Optimize this so it automatically calculates everything AHEAD of time
    if c == '>':
        match optimization_option:
            case 0:
                data_pos += 1
                if data_pos > len(data):
                    data_pos = 0

                debug_file.write(f"new data pointer: {data_pos}\n")
                lines.append(f"pointer += {1}")
            #TODO: FIX THIS
            case 1:
                amount_to_increase = 1

                while code_pos < len(code) and code[code_pos] == ">":
                    code_pos += 1
                    amount_to_increase += 1
                
                data_pos += amount_to_increase
                
                if data_pos > len(data):
                    data_pos = 0

                debug_file.write(f"new data pointer: {data_pos}\n")
                lines.append(f"pointer += {amount_to_increase-1}")

    elif c == '<':
        if data_pos != 0:
            data_pos -= 1
        lines.append(f"pointer -= {1}")

    elif c == '+':
        if d == 255:
            data[data_pos] = 0
        else:
            data[data_pos] += 1
        lines.append(f"memory[pointer] += {1}")
        lines.append("memory[pointer] = memory[pointer] % 256")
    elif c == '-':
        if d == 0:
            data[data_pos] = 255
        else:
            data[data_pos] -= 1
        lines.append(f"memory[pointer] -= {1}")
        lines.append("memory[pointer] = memory[pointer] % 256")
    elif c == '.':
        out(chr(d))
        lines.append('print(chr(memory[pointer]), end="")')
    elif c == ',':
        data[data_pos] = ord(sys.stdin.read(1))
        #ik i could probably do better, but eh
        input_code=f"""
        a = input()\n
        while len(a.replace(" ", "")) <= 0:\n
            a = input()\n
        memory[pointer] = ord(a[0])\n
        """
        lines.append(input_code)
    else:
        bracket, jmp = c
        if bracket == '[' and d == 0:
            step = 0
            code_pos = jmp
        elif bracket == ']' and d != 0:
            step = 0
            code_pos = jmp

    return (data, code_pos, data_pos, step)


def eval(code, data=[0 for i in range(9999)], d_pos=0):
    global c_pos
    while c_pos < len(code):
        (data, c_pos, d_pos, step) = eval_step(code, data, c_pos, d_pos)
        c_pos += step

if len(sys.argv) < 2:
    print("usage: python brainfuck.py file.bf")
    exit(1)
c_pos = 0
python_file = open("output.py", "w")
try:
    lines = ["import sys; memory = [0]*30000; pointer=0"] # init stuff

    with open(sys.argv[1], 'r') as infile:
        code = read(''.join(infile.readlines()))
        eval(code)

    for i in range(len(lines)):
        lines[i] += "\n" # automatically add new lines

    python_file.writelines(lines) # write them to a file
    python_file.close() # close
    debug_file.close()

except Exception:
    logging.exception("Error: ")
    debug_file.write(f"PROGRAM  CRASHED!, time of crash: {datetime.now()}\n")
    debug_file.close()
    python_file.close()
    exit(1)
