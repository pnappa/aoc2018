#include <stdio.h>
#include <assert.h>

/**
 * A decompiled version of the elf asm program again!
 * This time for day21's input
 */

//#define WAIT getchar();
#define WAIT ;
#define DUMP_REG printf("registers: [%d, %d, _, %d, %d, %d]\n", r0, r1, r3, r4, r5); WAIT
#define DEBUG_REG ;
#define DEBUG_REG DUMP_REG

int main() {
    int r0 = 0;
    int r1 = -1; // r1 is redundant
    int r2 = 0;
    int r3 = 0;
    //int r4 = 0; // register 4 is RIP
    int r5 = 0; // r5 is now redundant.

    do {
       r2 = r3 | 65536;
       r3 = 1397714;
instr8:;
       r3 += r2 & 255;
       r3 &= 16777215;
       r3 *= 65899;
       r3 &= 16777215;
       if (256 > r2) {
           goto instr28;
       }
       goto instr17;
instr17:;
        if (256 > r2) {
            goto instr26;
        }
        // addi 4 1 4
        goto instr27;
instr26:;
        r2 = 0;
instr27:;
        goto instr8;
instr28:;

    } while (r3 != r0);

    printf("finished!\n");
    return 0;
}
