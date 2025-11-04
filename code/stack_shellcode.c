/*
stack_shellcode.c
compile with: gcc -o stack_shellcode -fno-stack-protector -z execstack stack_shellcode.c
*/
#include <stdio.h>
#include <unistd.h>

void setup() {
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln() {
    char buffer[100];
    printf("buffer @ %p\n", buffer);
    printf("Enter some text: ");
    read(0, buffer, 200);

    
}

int main() {
    setup();
    vuln();
    return 0;
}
