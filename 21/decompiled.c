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
    int r1 = 0;
    int r2 = 0;
    int r3 = 0;
    //int r4 = 0; // register 4 is RIP
    int r5 = 0;

instr0:;
       r3 = 123;
instr1:;
        r3 &= 456;
instr2:;
        r3 = r3 == 72;
instr3:;
       if (r3 == 1) {
        goto instr5;
       }
instr4:;
       // loop in the shitty bitwise routine
       // if 123 & 456 != 72
       goto instr1;
instr5:;
       // reset register 3 after bitwise test
       r3 = 0;
instr6:;
       r2 = r3 | 65536;
instr7:;
       r3 = 1397714;
instr8:;
       r5 = r2 & 255;
instr9:;
       r3 += r5;
instr10:;
        r3 &= 16777215;
instr11:;
        r3 *= 65899;
instr12:;
        r3 &= 16777215;
instr13:;
        r5 = 256 > r2;
instr14:;
        if (r5 == 1) {
            goto instr16;
        }
instr15:;
        goto instr17;
instr16:;
        goto instr28;
instr17:;
        r5 = 0;
instr18:;
        r1 = r5 + 1;
instr19:;
        r1 *= 256;
instr20:;
        r1 = r1 > r2;
instr21:;
        if (r1 == 1) {
            goto instr23;
        }
instr22:;
        // addi 4 1 4
        goto instr27;
instr23:;
        // seti 25 2 4
        goto instr26;
instr24:;
        r5 += 1;
instr25:;
        // seti 17 0 4
        goto instr18;
instr26:;
        r2 = r5;
instr27:;
        goto instr8;
instr28:;
        r5 = r3 == r0;         
instr29:;
        // addr 5 4 4 
        // this finished the program as we go to instruction 31.
        if (r5 == 1) {
            printf("finished!\n");
            return 0;
        }
instr30:;
        // seti 5 8 4
        goto instr6;
}
