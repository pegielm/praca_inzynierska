/*
buffer_overflow.c
compile with: gcc -o buffer_overflow -std=c17 -fno-stack-protector -no-pie buffer_overflow.c
*/
#include <stdio.h>
void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}
int win(){
    puts("win!");
}
int main() {
    setup();
    int target = 0xcafebabe;
    char buffer[10];
    printf("Enter some text: ");
    gets(buffer);
    if (target == 0xdeadbeef){
        puts("success!");
    }
    else {
        printf("target: 0x%x\n", target);
    }
    return 0;
}