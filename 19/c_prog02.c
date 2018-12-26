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
#define DUMP_REG printf("registers: [%d, %d, _, %d, %d, %d]\n", r0, r1, r3, r4, r5); WAIT
#define DEBUG_REG ;
//#define DEBUG_REG DUMP_REG

void init(int r0, int* r1, int* r3, int* r4, int* r5) {
    // future assertion for potential optimisation
    // ..i think its true for this program..?
    assert(*r3 == 0 && *r5 == 0);
    // part1, part2
    assert(r0 == 0 || r0 == 1);

    *r3 = ((2*2)*19*11);

    *r5 = (2*22 + 8);

    *r3 += *r5;

    // if the register 0 is preset to 0, we next perform goto instr1, which is equivalent to leaving this fn
    if (r0 == 0) return;

    *r5 = (27*28 + 29)*30*14*32;

    *r3 += *r5;

    return;
}

// an equivalent C program of the elf-code program (i hope...)
int main() {
    // registers 0-5 (ignore register r2 though, it's the RIP)
    int r1 = 0;
    //int r2 = 0;
    int r3 = 0;
    int r4 = 0;
    int r5 = 0; // TODO: remove  this register

    int result = 0; //part 1
    //int result = 1; // part2

    // the mini subroutine of rip instr17 onwards
    init(result, &r1, &r3, &r4, &r5);

    // OBSERVATIONS: 
    //      - r5 is never used in a result except as a condition variable
    //          (or in the init, but it's assigned/added to r3 always)

    result = 0;

    r4 = 1;
    DEBUG_REG;
    do {
        r1 = 1;
        DEBUG_REG;

        do {
            if (r4*r1 == r3) {
                result += r4;
            }

            r1 += 1;
            DEBUG_REG;

        } while (r1 <= r3);

        r4 += 1;
        DEBUG_REG;

    } while (r4 <= r3);

    // XXX: this is how the program 
    // terminates doood
    printf("program finished! squaring rip -> dead\n");
    printf("result: %d\n", result);
    //DUMP_REG;
    return 0;
}
