#include <stdio.h>
#include <assert.h>

/**
 * A decompiled version of the elf asm program again!
 * This time for day21's input
 */

//#define WAIT getchar();
#define WAIT ;
#define DUMP_REG printf("registers: [%d, %d, _, %d, %d, %d]\n", r0, r1, r2, r3, r5); WAIT
#define DEBUG_REG ;
#define DEBUG_REG DUMP_REG

int main() {
    int r0 = 0;
    int r1 = 0;
    int r2 = 0;
    int r3 = 0;
    //int r4 = 0; // register 4 is RIP
    int r5 = 0;

    r3 = 123;
instr1:;
       r3 &= 456;
       r3 = r3 == 72;
       if (r3 == 1) {
           puts("bitwise is not broken");
           goto instr5;
       }
       // loop in the shitty bitwise routine
       // if 123 & 456 != 72
       goto instr1;
instr5:;
       // reset register 3 after bitwise test
       r3 = 0;
       r2 = r3 | 65536;
       r3 = 1397714;
instr8:;
       r5 = r2 & 255;
       r3 += r5;
       r3 &= 16777215;
       r3 *= 65899;
       r3 &= 16777215;
       r5 = 256 > r2;
       if (r5 == 1) {
           goto instr16;
       }
       goto instr17;
instr16:;
        goto instr28;
instr17:;
        r5 = 0;
instr18:;
        r1 = r5 + 1;
        r1 *= 256;
        r1 = r1 > r2;
        if (r1 == 1) {
            goto instr23;
        }
        // addi 4 1 4 (as instr22)
        goto instr27;
instr23:;
        // seti 25 2 4
        goto instr26;
        r5 += 1;
        // seti 17 0 4
        goto instr18;
instr26:;
        r2 = r5;
instr27:;
        goto instr8;
instr28:;
        r5 = r3 == r0;         
        // addr 5 4 4
        // go forward 6 instructions!
        // this is the terminating clause
        printf("finished!");
        return 0;

        // dead code
        // seti 5 8 4
        // goto instr6;
}
