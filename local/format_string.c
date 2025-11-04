/*
format_string.c
compile with: gcc -Wl,-z,relro -o format_string format_string.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

void setup() {
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int win() {
    puts("win!");
    system("/bin/sh");
}

int main() {
    setup();
    unsigned int target = 0xcafebabe;
    char buf[256];

    printf("\nEnter some text: ");
    scanf("%255s", buf);
    printf(buf);

    printf("\nEnter some text: ");
    scanf("%255s", buf);
    printf(buf);

    if (target == 0xdeadbeef) {
        puts("success!");
    } else {
        printf("target: 0x%x\n", target);
    }

    return 0;
}