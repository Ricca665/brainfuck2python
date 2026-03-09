-# brainfuck2python compiler
This is a silly project of mine that is like "what if you could convert brainfuck code, from an already
slow language, into something even slower?"
so i came up with this

(based on the brainfuck.py interpreter made by pocmo!)

-# how 2 use
```
python main.py ./file.bf
python output.py
```

So what i had to make it work is literally made every instruction add the corresponding BF instruction (so > becomes pointer += 1)
the compiled result is a LOT slower and heavier than the original code since something like this:
```
>+.
```
gets turned into smth like this:
```
memory = [0] * 30000; pointer = 0
pointer += 1
memory[pointer] += 1
memory[pointer] = memory[pointer] % 256 # make it overflow
print(chr(memory[pointer]), end="")
```
so of course it's a lot slower

future features
- [ ] add more optimization options (0: nothing, 1: stuff like >>>>> gets turned into pointer += 5, 2: precompute memory and just execute the moving pointers part)
