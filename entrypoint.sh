#!/bin/bash


service ssh start
echo "[+] SSH service started (port 22 -> 2222)"



socat TCP-LISTEN:9001,reuseaddr,fork EXEC:"/challs/buffer_overflow_2",su=user_buffer_overflow_2 &
socat TCP-LISTEN:9002,reuseaddr,fork EXEC:"/challs/rop",su=user_rop &
socat TCP-LISTEN:9003,reuseaddr,fork EXEC:"/challs/rop_2",su=user_rop_2 &
socat TCP-LISTEN:9004,reuseaddr,fork EXEC:"/challs/ret2libc",su=user_ret2libc &
socat TCP-LISTEN:9005,reuseaddr,fork EXEC:"/challs/format_string",su=user_format_string &
socat TCP-LISTEN:9006,reuseaddr,fork EXEC:"/challs/shellcode",su=user_shellcode &
socat TCP-LISTEN:9007,reuseaddr,fork EXEC:"/challs/stack_shellcode",su=user_stack_shellcode &

echo "[+] all services started!"
echo ""
echo "=== server running ==="
echo "SSH access:        -> ssh ctf@localhost -p 2222 (password: ctf)"
echo ""
echo "challenge Ports:"
echo "  buffer_overflow_2  -> port 9001"
echo "  rop                -> port 9002"
echo "  rop_2              -> port 9003"
echo "  ret2libc           -> port 9004"
echo "  format_string      -> port 9005"
echo "  shellcode          -> port 9006"
echo "  stack_shellcode    -> port 9007"
echo "===================================="


tail -f /dev/null
