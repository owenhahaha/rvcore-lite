golden_path = "sim/1_alu_golden.txt"
result_path = "sim/1_alu_result.txt"

with open(golden_path, 'r') as f_gold, open(result_path, 'r') as f_result:
    golden_lines = f_gold.readlines()
    result_lines = f_result.readlines()

all_passed = True
fail_count = 0
max_lines = max(len(golden_lines), len(result_lines))
for i in range(max_lines):
    g_line = golden_lines[i].strip()
    r_line = result_lines[i].strip()

    if g_line != r_line:
        all_passed = False
        fail_count += 1
        print(f"[\033[31mFAIL\033[0m] Mismatch at line {i+1}:  Golden: {g_line},  Result: {r_line}")

if all_passed:
    print("################################################")
    print("##### \033[32mCongratulation!!! Simulation PASS!!!\033[0m #####")
    print("################################################")
else:
    print(f"##################################################")
    print(f"##### \033[31mFailed!!! You have {fail_count} errors\033[0m #####")
    print(f"##################################################")