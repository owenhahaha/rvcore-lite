# gen_alu_test.py
import random

def negate(bit_stream:str) -> str:
    out = ""
    cin_flag = True
    for b in bit_stream[::-1]:
        if cin_flag:
            if b == "0":
                out = "0" + out
            else:
                out = "1" + out
                cin_flag = False
        else:
            if b == "0":
                out = "1" + out
            else:
                out = "0" + out
    return out

def two_comp(num:int, bits:int) -> str:
    out = ""
    if num >= 0:
        for _ in range(bits):
            b = str(num % 2)
            out = b + out
            num = int(num / 2)
        return out
    else:
        for _ in range(bits):
            b = str(num % 2)
            out = b + out
            num = int(num / 2)
        out = negate(out)
        return out

def two_2_int(bit_stream:str, index1:int, index2:int, signed:bool = True) -> int:
    index1 = len(bit_stream) - index1 - 1
    index2 = len(bit_stream) - index2 - 1
    out = 0
    n = 0
    while index1 <= index2 and signed:
        if bit_stream[index2] == "1" and index1 != index2:
            out = out + 2 ** n
        elif bit_stream[index2] == "1" and index1 == index2:
            out = out - 2 ** n
        index2 -= 1
        n += 1
    while index1 <= index2 and (not signed):
        if bit_stream[index2] == "1":
            out = out + 2 ** n
        index2 -= 1
        n += 1
    return out

def two_2_hex(bit_stream:str) -> str:
    table = {"0000":"0",
             "0001":"1",
             "0010":"2",
             "0011":"3",
             "0100":"4",
             "0101":"5",
             "0110":"6",
             "0111":"7",
             "1000":"8",
             "1001":"9",
             "1010":"a",
             "1011":"b",
             "1100":"c",
             "1101":"d",
             "1110":"e",
             "1111":"f"}
    out = ""
    while len(bit_stream) > 0:
        out = out + table[bit_stream[0:4]]
        bit_stream = bit_stream[4:]
    return out

def shift(bit_stream:str, amount:int, type:str) -> str:
    if type == "LL":
        out = bit_stream[amount:]
        for _ in range(amount):
            out = out + "0"
    elif type == "RL":
        out = bit_stream[:len(bit_stream)-amount]
        for _ in range(amount):
            out = "0" + out
    elif type == "RA":
        signed_bit = bit_stream[0]
        out = bit_stream[:len(bit_stream)-amount]
        for _ in range(amount):
            out = signed_bit + out
    else:
        out = ""
        print("Shift type invalid")
    return out

# set random seed
random.seed(100)

# N tests
N = 1000

with open("sim/1_alu_test.txt", "w") as f_test, open("sim/1_alu_golden.txt", "w") as f_gold:
    for _ in range(N):
        a = random.getrandbits(32)
        b = random.getrandbits(32)
        sel = random.randint(0, 9)
        a_int = two_2_int(two_comp(a, 32), 31, 0)
        b_int = two_2_int(two_comp(b, 32), 31, 0)
        shift_amount = two_2_int(two_comp(b, 32), 4, 0, False)
        if sel == 0:
            result = a_int + b_int
        elif sel == 1:
            result = a_int - b_int
        elif sel == 2:
            result = a & b
        elif sel == 3:
            result = a | b
        elif sel == 4:
            result = a ^ b
        elif sel == 5:
            result = two_2_int(shift(two_comp(a, 32), shift_amount, "LL"), 31, 0)
        elif sel == 6:
            result = two_2_int(shift(two_comp(a, 32), shift_amount, "RL"), 31, 0)
        elif sel == 7:
            result = two_2_int(shift(two_comp(a, 32), shift_amount, "RA"), 31, 0)
        elif sel == 8:
            a = two_comp(a, 32)
            b = two_comp(b, 32)
            a = two_2_int(a, 31, 0)
            b = two_2_int(b, 31, 0)
            result = a < b
        elif sel == 9:
            result = a < b
        f_test.write(f"{two_2_hex(two_comp(a, 32))} {two_2_hex(two_comp(b, 32))} {sel:x}\n")
        f_gold.write(f"{two_2_hex(two_comp(result, 32))}\n")
