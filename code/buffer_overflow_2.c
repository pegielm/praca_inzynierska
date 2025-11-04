/*
buffer_overflow_2.c
compile with: gcc -o buffer_overflow_2 -std=c17 -fno-stack-protector -no-pie buffer_overflow_2.c
*/
#include <stdio.h>
#include <stdlib.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win() {
    puts("win!");
    system("/bin/sh");
}

void vulnerable() {
    char buffer[32];
    puts("Enter some text: ");
    gets(buffer);
    puts("You entered: ");
    puts(buffer);
}

int main() {
    setup();
    vulnerable();
    puts("Exited normally");
    return 0;
}