/*
rop.c
compile with: gcc -o ret2libc -std=c17 -fno-stack-protector ret2libc.c
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vulnerable() {
    char buffer[16];
    
    puts("Enter some text: ");
    read(0, buffer, 200);
}

void leak(){
    unsigned long array[2] = {0x11111111, 0x22222222};
    int (*myputs)(const char*) = puts;   
    void (*vuln)() = vulnerable;
    char input[10];
    for(int i=0; i<2; i++){
        myputs("Enter index to lookup: ");
        fgets(input, sizeof(input), stdin);
        int index = atoi(input);
        printf("Value at index %d: %lx\n", index, array[index]);
    }
    // call vulne
    vuln();
}



int main() {
    setup();
    leak();
    puts("exited normally");
    return 0;
}
