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
    int r5 = 0;

    // OMITTED: bitwise test code.
    // reset register 3 after bitwise test
    r3 = 0;
    do {
       r2 = r3 | 65536;
       r3 = 1397714;
instr8:;
       // XXX: we can remove r5, as it's 
       // not used after this basic block.
       r5 = r2 & 255;
       r3 += r5;
       r3 &= 16777215;
       r3 *= 65899;
       r3 &= 16777215;
       r5 = 256 > r2;
       if (r5 == 1) {
           goto instr28;
       }
       goto instr17;
instr17:;
        r5 = 0;
        if ((r5 + 1)*256 > r2) {
            goto instr23;
        }
        // addi 4 1 4
        goto instr27;
instr23:;
        // seti 25 2 4
        goto instr26;
        //r5 += 1;
        //// seti 17 0 4
        //goto instr18;
instr26:;
        r2 = r5;
instr27:;
        goto instr8;
instr28:;

    } while (r3 != r0);

    printf("finished!\n");
    return 0;
}
