#include <stdio.h>
#include <assert.h>

/**
 * LETS OPTIMISE
 * LETS GO
 *
 * Steps following:
 *  - remove all un-necessary goto-labels
 *  - move init code into a fn
 *  - replace gotos with for/while loops and functions
 *  - rename variables to be useful (context dependent)
 */

//#define WAIT getchar();
#define WAIT ;
#define DUMP_REG ;
//#define DUMP_REG printf("registers: [%d, %d, _, %d, %d, %d]\n", r0, r1, r3, r4, r5); WAIT

void init(int* r0, int* r1, int* r3, int* r4, int* r5) {
    // future assertion for potential optimisation
    // ..i think its true for this program..?
    assert(*r3 == 0 && *r5 == 0);

    *r3 += 2;
    *r3 *= *r3;
    *r3 *= 19;
    *r3 *= 11;

    *r5 += 2;
    *r5 *= 22;
    *r5 += 8;

    *r3 += *r5;

    // if the register 0 is preset to 0, we next perform goto instr1, which is equivalent to leaving this fn
    if (*r0 == 0) return;

    *r5 = 27;
    *r5 *= 28;
    *r5 += 29;
    *r5 *= 30;
    *r5 *= 14;
    *r5 *= 32;
    *r3 += *r5;
    *r0 = 0;

    return;
}

// an equivalent C program of the elf-code program (i hope...)
int main() {
    // registers 0-5 (ignore register r2 though, it's the RIP)
    int r0 = 0;
    int r1 = 0;
    //int r2 = 0;
    int r3 = 0;
    int r4 = 0;
    int r5 = 0;

    // the mini subroutine of rip instr17 onwards
    init(&r0, &r1, &r3, &r4, &r4);

       r4 = 1;
       DUMP_REG
instr2:;
       r1 = 1;
       DUMP_REG
instr3:;
       r5 = r4 * r1;
       DUMP_REG

       r5 = r5 == r3;
       DUMP_REG
       if (r5 == 1) {
            goto instr7;
       }
       goto instr8;
instr7:;
       r0 += r4;
       DUMP_REG
instr8:;
       r1 += 1;
       DUMP_REG

       // gtrr 1 3 5
       r5 = r1 > r3;
       DUMP_REG

        // addr 2 5 2
       if (r5 == 1) {
            goto instr12;
       }

        // seti 2 6 2
        goto instr3;
instr12:;
        r4 += 1;
       DUMP_REG

        r5 = r4 > r3;
       DUMP_REG

        if (r5 == 1) {
            goto instr16;
        }

        goto instr2;
instr16:;
        // XXX: this is how the program 
        // terminates doood
        printf("program finished! squaring rip -> dead\n");
       DUMP_REG
        return 0;
}
