import sys

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



def eval_step(code, data, code_pos, data_pos, out=sys.stdout.write):
    c = code[code_pos]
    d = data[data_pos]
    step = 1
    #print(f"codepos{code_pos}")
    if c == '>':
        data_pos = data_pos + 1
        if data_pos > len(data):
            data_pos = 0

        lines.append(f"pointer += {1}")
        
    elif c == '<':
        if data_pos != 0:
            data_pos -= 1
        lines.append("pointer -= 1")

    elif c == '+':
        if d == 255:
            data[data_pos] = 0
        else:
            data[data_pos] += 1
        lines.append("memory[pointer] += 1")
        lines.append("memory[pointer] = memory[pointer] % 256")
    elif c == '-':
        if d == 0:
            data[data_pos] = 255
        else:
            data[data_pos] -= 1
        lines.append("memory[pointer] -= 1")
        lines.append("memory[pointer] = memory[pointer] % 256")
    elif c == '.':
        out(chr(d))
        lines.append('print(chr(memory[pointer]), end="")')
    elif c == ',':
        data[data_pos] = ord(sys.stdin.read(1))
        input_code=f"""
        a = input().split("")\n
        while len(a) <= 0:\n
            a = input().split()\n
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
    lines = ["import sys; memory = [0]*30000; pointer=0"]

    with open(sys.argv[1], 'r') as infile:
        code = read(''.join(infile.readlines()))
        eval(code)

    for i in range(len(lines)):
        lines[i] += "\n" # automatically add returns
    python_file.writelines(lines)
    python_file.close()

except Exception as e:
    print(f"Error: {e}")
    python_file.close()
    exit(1)
