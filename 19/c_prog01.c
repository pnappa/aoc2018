#include <stdio.h>
#include <assert.h>

//#define WAIT getchar();
#define WAIT ;
#define DUMP_REG printf("registers: [%d, %d, _, %d, %d, %d]\n", r0, r1, r3, r4, r5); WAIT

// an equivalent C program of the elf-code program (i hope...)
int main() {
    // registers 0-5 (ignore register c though, it's the RIP)
    int r0 = 0;
    int r1 = 0;
    //int c = 0;
    int r3 = 0;
    int r4 = 0;
    int r5 = 0;

instr0:;
       goto instr17;
instr1:;
       r4 = 1;
       DUMP_REG
instr2:;
       r1 = 1;
       DUMP_REG
instr3:;
       r5 = r4 * r1;
       DUMP_REG
instr4:;
       r5 = r5 == r3;
       DUMP_REG
instr5:;
       if (r5 == 1) {
            goto instr7;
       }
instr6:;
       goto instr8;
instr7:;
       r0 += r4;
       DUMP_REG
instr8:;
       r1 += 1;
       DUMP_REG
instr9:;
       // gtrr 1 3 5
       r5 = r1 > r3;
       DUMP_REG
instr10:;
        // addr 2 5 2
       if (r5 == 1) {
            goto instr12;
       }
instr11:;
        // seti 2 6 2
        goto instr3;
instr12:;
        r4 += 1;
       DUMP_REG
instr13:;
        r5 = r4 > r3;
       DUMP_REG
instr14:;
        if (r5 == 1) {
            goto instr16;
        }
instr15:;
        goto instr2;
instr16:;
        // XXX: this is how the program 
        // terminates doood
        printf("program finished! squaring rip -> dead\n");
       DUMP_REG
        return 0;
instr17:;
        // addi 3 2 3???
        r3 += 2;
       DUMP_REG
instr18:;
        // mulr 3 3 3
        r3 *= r3;
       DUMP_REG
instr19:;
        // mulr 2 3 3
        r3 *= 19;
       DUMP_REG
instr20:;
        // muli 3 11 3
        r3 *= 11;
       DUMP_REG
instr21:;
        // addi 5 2 5
        r5 += 2;
       DUMP_REG
instr22:;
        // mulr 5 2 5
        r5 *= 22;
       DUMP_REG
instr23:;
        // addi 5 8 5
        r5 += 8;
       DUMP_REG
instr24:;
        r3 += r5;
       DUMP_REG
instr25:;
        // ???
        // addr 2 0 2
        // fuck, i really hope r0 is not changed anywhere except at the start before reaching here
        assert((r0 == 0 || r0 == 1) && "hum, assumption didn't hold true");
        if (r0 == 0) {
            goto instr26;
        } else if (r0 == 1) {
            goto instr27;
        }
instr26:;
       // seti 0 4 2
       goto instr1;
instr27:;
        // setr 2 5 5
        r5 = 27;
       DUMP_REG
instr28:;
        // mulr 5 2 5
        r5 *= 28;
       DUMP_REG
instr29:;
       r5 += 29;
       DUMP_REG
instr30:;
       r5 *= 30;
       DUMP_REG
instr31:;
       r5 *= 14;
       DUMP_REG
instr32:;
       r5 *= 32;
       DUMP_REG
instr33:;
       r3 += r5;
       DUMP_REG
instr34:;
       r0 = 0;
       DUMP_REG
instr35:;
       goto instr1;
}
