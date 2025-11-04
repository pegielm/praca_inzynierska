/*
rop.c
compile with: gcc -o rop -std=c17 -fno-stack-protector -no-pie rop.c
*/
#include <stdio.h>
#include <stdlib.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win(unsigned long arg1, unsigned long arg2) {
    printf("win() called with arg1=0x%lx, arg2=0x%lx\n", arg1, arg2);
    
    if (arg1 == 0xdeadbeef && arg2 == 0xcafebabe) {
        puts("success!");
        system("/bin/sh");
    } else {
        puts("wrong arguments");
    }
}

void gadgets(void) {
    __asm__("pop %rdi; ret");
    __asm__("pop %rsi; ret");
}

void vulnerable() {
    char buffer[32];
    puts("Enter some text: ");
    gets(buffer);
}

int main() {
    setup();
    vulnerable();
    puts("exited normally");
    return 0;
}
