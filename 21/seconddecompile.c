#include <stdio.h>
#include <assert.h>
#include <inttypes.h>

/**
 * Fuck, the first decompiled program isn't equivalent...?
 */

int num_instructions_executed = 0;
#define WAIT ;
//#define WAIT getchar();
#define DUMP_REG printf("registers: [%" PRId64 ", %" PRId64 ", %" PRId64 ", %" PRId64 ", _, %" PRId64 "] - line: %d\n", r0, r1, r2, r3, r5, __LINE__); WAIT
#define DEBUG_REG ;
//#define DEBUG_REG DUMP_REG
#define INSTR(x) printf("instr %s, line %d - NUM: %d\n", x, __LINE__, ++num_instructions_executed);

int main() {

    int64_t r0 = 0;
    int64_t r1 = 0;
    int64_t r2 = 0;
    int64_t r3 = 0;
    //int64_t r4 = 0;
    int64_t r5 = 0;

    /** bitwise test routine **/
    INSTR("seti 123 0 3");
    r3 = 123;
    DEBUG_REG;
instr1:
    INSTR("bani 3 456 3");
    r3 = r3 & 456;
    DEBUG_REG;
    INSTR("eqri 3 72 3");
    r3 = r3 == 72;
    DEBUG_REG;
    INSTR("addr 3 4 4");
    if (r3 == 1) goto instr5;
    INSTR("seti 0 0 4");
    goto instr1;
    /** end bitwise routine **/

instr5:
    INSTR("seti 0 2 3");
    r3 = 0;
    DEBUG_REG;
instr6:
    INSTR("bori 3 65536 2");
    r2 = r3 | 65536;
    DEBUG_REG;

    INSTR("seti 1397714 1 3");
    r3 = 1397714;
    DEBUG_REG;

instr8:
    INSTR("bani 2 255 5");
    r5 = r2 & 255;
    DEBUG_REG;

    INSTR("addr 3 5 3");
    r3 += r5;
    DEBUG_REG;

    INSTR("bani 3 16777215 3");
    r3 = r3 & 16777215;
    DEBUG_REG;

    INSTR("muli 3 65899 3");
    r3 *= 65899;
    DEBUG_REG;

    INSTR("bani 3 16777215 3");
    r3 &= 16777215;
    DEBUG_REG;

    INSTR("gtir 256 2 5");
    r5 = 256 > r2;
    DEBUG_REG;

    INSTR("addr 5 4 4");
    if (r5 == 1) goto instr16;
    DEBUG_REG;

    INSTR("addi 4 1 4");
    goto instr17;

instr16:
    INSTR("seti 27 6 4");
    goto instr28;

instr17:
    INSTR("seti 0 6 5");
    r5 = 0;
    DEBUG_REG;

instr18:
    INSTR("addi 5 1 1");
    r1 = r5 + 1;
    DEBUG_REG;

    INSTR("muli 1 256 1");
    r1 *= 256; 
    DEBUG_REG;

    INSTR("gtrr 1 2 1");
    r1 = r1 > r2;
    DEBUG_REG;

    INSTR("addr 1 4 4");
    if (r1 == 1) goto instr23;

    INSTR("addi 4 1 4");
    goto instr24;

instr23:
    INSTR("seti 25 2 4");
    goto instr26;

instr24:
    INSTR("addi 5 1 5");
    r5 += 1;
    DEBUG_REG;

    INSTR("seti 17 0 4");
    goto instr18;

instr26:
    INSTR("setr 5 7 2");
    r2 = r5;
    DEBUG_REG;

    INSTR("seti 7 4 4");
    goto instr8;

instr28:
    INSTR("eqrr 3 0 5");
    r5 = r3 == r0;
    DEBUG_REG;

    INSTR("addr 5 4 4");

    if (r5 == 1) {
        puts("finished!");
        return 0;
    }

    INSTR("seti 5 8 4");
    goto instr6;
}
