FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    build-essential \
    openssh-server \
    vim \
    gdb \
    python3 \
    python3-pip \
    netcat \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pwntools

RUN useradd -m user_buffer_overflow_2 && \
    useradd -m user_rop && \
    useradd -m user_rop_2 && \
    useradd -m user_ret2libc && \
    useradd -m user_format_string && \
    useradd -m user_shellcode && \
    useradd -m user_stack_shellcode

RUN useradd -m -s /bin/bash ctf && \
    echo 'ctf:ctf' | chpasswd && \
    usermod -aG sudo ctf 2>/dev/null || true

RUN mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo "AllowUsers ctf" >> /etc/ssh/sshd_config


RUN mkdir -p /challs /code /source_code

COPY code/ /tmp/code/
RUN cp /tmp/code/*.c /tmp/ && \
    cp /tmp/code/*.c /source_code/

RUN gcc -o /challs/buffer_overflow_2 -std=c17 -fno-stack-protector -no-pie /tmp/buffer_overflow_2.c && \
    gcc -o /challs/rop -std=c17 -fno-stack-protector -no-pie /tmp/rop.c && \
    gcc -o /challs/rop_2 -std=c17 -fno-stack-protector -no-pie /tmp/rop_2.c && \
    gcc -o /challs/ret2libc -std=c17 -fno-stack-protector /tmp/ret2libc.c && \
    gcc -o /challs/format_string -Wl,-z,relro  /tmp/format_string.c && \
    gcc -o /challs/shellcode -fno-stack-protector /tmp/shellcode.c && \
    gcc -o /challs/stack_shellcode -fno-stack-protector -z execstack /tmp/stack_shellcode.c && \
    rm -rf /tmp/*.c

RUN chmod 755 /challs/*

RUN cp /lib/x86_64-linux-gnu/libc.so.6 /code/ && \
    cp /lib64/ld-linux-x86-64.so.2 /code/ && \
    chmod 644 /code/*

RUN echo "flag{buffer_overflow_2_9c4e7ab2f6d158a3}" > /home/user_buffer_overflow_2/flag.txt && \
    echo "flag{rop_challenge_7d3a5f81b9e246c0}" > /home/user_rop/flag.txt && \
    echo "flag{rop_2_syscall_2b8f4e9a3c7d156f}" > /home/user_rop_2/flag.txt && \
    echo "flag{ret2libc_6e2c9f7a4b5d183e}" > /home/user_ret2libc/flag.txt && \
    echo "flag{format_string_4a9d7e2f8b3c156a}" > /home/user_format_string/flag.txt && \
    echo "flag{shellcode_exec_3f8b5e1a9d2c674e}" > /home/user_shellcode/flag.txt && \
    echo "flag{stack_shellcode_1c7e4b9f2a8d356e}" > /home/user_stack_shellcode/flag.txt && \
    chown user_buffer_overflow_2:user_buffer_overflow_2 /home/user_buffer_overflow_2/flag.txt && \
    chown user_rop:user_rop /home/user_rop/flag.txt && \
    chown user_rop_2:user_rop_2 /home/user_rop_2/flag.txt && \
    chown user_ret2libc:user_ret2libc /home/user_ret2libc/flag.txt && \
    chown user_format_string:user_format_string /home/user_format_string/flag.txt && \
    chown user_shellcode:user_shellcode /home/user_shellcode/flag.txt && \
    chown user_stack_shellcode:user_stack_shellcode /home/user_stack_shellcode/flag.txt && \
    chmod 400 /home/user_*/flag.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN echo "challenges" > /home/ctf/README.txt && \
    echo "==============" >> /home/ctf/README.txt && \
    echo "" >> /home/ctf/README.txt && \
    echo "challenge Ports:" >> /home/ctf/README.txt && \
    echo "  buffer_overflow_2 -> nc localhost 9001" >> /home/ctf/README.txt && \
    echo "  rop               -> nc localhost 9002" >> /home/ctf/README.txt && \
    echo "  rop_2             -> nc localhost 9003" >> /home/ctf/README.txt && \
    echo "  ret2libc          -> nc localhost 9004" >> /home/ctf/README.txt && \
    echo "  format_string     -> nc localhost 9005" >> /home/ctf/README.txt && \
    echo "  shellcode         -> nc localhost 9006" >> /home/ctf/README.txt && \
    echo "  stack_shellcode   -> nc localhost 9007" >> /home/ctf/README.txt && \
    echo "" >> /home/ctf/README.txt && \
    echo "binaries: /challs/" >> /home/ctf/README.txt && \
    echo "source code: /source_code/" >> /home/ctf/README.txt && \
    echo "libc: /code/libc.so.6" >> /home/ctf/README.txt && \
    echo "" >> /home/ctf/README.txt && \
    echo "SSH access: ssh ctf@localhost -p 2222 (password: ctf)" >> /home/ctf/README.txt && \
    chown ctf:ctf /home/ctf/README.txt

EXPOSE 9001 9002 9003 9004 9005 9006 9007 22

ENTRYPOINT ["/entrypoint.sh"]
