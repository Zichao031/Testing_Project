import re



def main():
    with open("new_walkthrough.txt", "r") as f, open("results.txt", "w") as f1:
        results = f.readlines()
        line_num = 0
        hash_table = {}
        for res in results:
            if not res.startswith("suite_size"):
                print(res)
                f1.write(res)
                curr_program = res.replace('\n', '')
                hash_table[curr_program] = 0
                continue
            matches = re.findall('\d+', res)
            print(matches)
            suite_size = int(matches[0])
            false_num = int(matches[1])
            if false_num > 0:
                fault = 1
                hash_table[curr_program] += 1
            else:
                fault = 0
                hash_table[curr_program] += 0
            f1.write("suite_size: " + str(suite_size) + "  " + "false_num: " + str(false_num) + "  "
                      +"fault number: "+ str(hash_table[curr_program]) + "\n")

        f1.write("Summary\n")
        for key, value in hash_table.items():
            f1.write(key + ",   " + str(value) + "\n")

    f1.close()
    f.close()

if __name__ == "__main__":
    main()
#
