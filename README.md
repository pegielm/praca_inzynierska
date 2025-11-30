## setup

```bash
docker compose build

docker compose up -d
```

## getting challange binaries

```
docker build -f Dockerfile.build -t ctf-builder .

docker run --rm -v "$(pwd)/local:/out" ctf-builder
```

## challenge Ports

| Challenge         | Port | Command                  |
|-------------------|------|--------------------------|
| buffer_overflow_2 | 9001 | `nc localhost 9001`      |
| rop               | 9002 | `nc localhost 9002`      |
| rop_2             | 9003 | `nc localhost 9003`      |
| ret2libc          | 9004 | `nc localhost 9004`      |
| format_string     | 9005 | `nc localhost 9005`      |
| shellcode         | 9006 | `nc localhost 9006`      |
| stack_shellcode   | 9007 | `nc localhost 9007`      |

## running exploits

in `/local/` there are exploits scripts for each challenge.
