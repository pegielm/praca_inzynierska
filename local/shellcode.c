/*
shellcode.c
compile with: gcc -o shellcode -fno-stack-protector shellcode.c
*/
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>

void setup() {
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    setup();
    
    void *mem = mmap(0, 0x1000, 
                     PROT_READ | PROT_WRITE | PROT_EXEC,
                     MAP_PRIVATE | MAP_ANON, -1, 0);
    

    printf("shellcode: ");
    read(0, mem, 100);
    
    ((void(*)())mem)();
    
    return 0;
}