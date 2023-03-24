import gzip
import json
import os
import re
import random

directory = ['printtokens', 'printtokens2', 'replace', 'schedule', 'schedule2', 'tcas', 'totinfo']
prioritizations = ['random', 'total_coverage']
criterias = ['statements', 'branches']
benchmarks = {}
tot_num = {}


def cal_tot(benchmark):
    json_file = gzip.open("{0}/{0}.gcov.json.gz".format(benchmark), "r")
    json_data = json.loads(json_file.read())
    branch_num = 0
    state_num = 0
    tot_num[benchmark] = {}
    for file in json_data['files']:
        for line in file['lines']:
            for branch in line['branches']:
                branch_num += 1
            state_num += 1
        #
    #
    tot_num[benchmark]['branches'] = branch_num
    tot_num[benchmark]['statements'] = state_num


def parse(benchmark):
    json_file = gzip.open("{0}/{0}.gcov.json.gz".format(benchmark), "r")
    json_data = json.loads(json_file.read())
    branch_num = 0
    statements = set()
    branches = set()
    parsed_data = {}
    # print(json_data)
    for file in json_data['files']:
        for line in file['lines']:
            for branch in line['branches']:
                branch['id'] = branch_num
                branch_num += 1
                if (branch['count'] > 0): branches.add(branch['id'])
            #
            if (line['count'] > 0): statements.add(line['line_number'])
        #
    #
    # print(branch_num)
    parsed_data['statements'] = list(statements)
    parsed_data['branches'] = list(branches)
    return parsed_data


#

def grip_one_test(benchmark, test, add=True):
    if (benchmark == "replace" or benchmark == "totinfo"):
        os.system(
            "cd {0} && gcc -Wno-return-type -w -g -o {0} {0}.c -lm -fprofile-arcs -ftest-coverage".format(benchmark))
    else:
        os.system("cd {0} && gcc -Wno-return-type -w -g -o {0} {0}.c -fprofile-arcs -ftest-coverage".format(benchmark))
    #
    os.system("cd {0} && ./{0} {1}".format(benchmark, test));
    os.system("cd {0} && gcov -b -j {0}.c".format(benchmark));
    if (add):
        parsed_data = parse(benchmark);
        parsed_data['body'] = test  # origin content of the test
        # print(parsed_data)
        benchmarks[benchmark]['tests'].append(parsed_data);
    else:
        cal_tot(benchmark)
    os.system("rm {0}/{0}.gcda".format(benchmark));


def grip_data(benchmark):
    benchmarks[benchmark] = {}
    benchmarks[benchmark]['tests'] = []
    # tot =30
    with open(benchmark + "/universe.txt", "r") as f:
        tests = f.readlines()
        grip_one_test(benchmark, tests[0], False)
        for test in tests:
            # tot-=1
            # if(tot<0): break
            grip_one_test(benchmark, test)
        #
    #
    f.close()
    os.system("rm {0}/{0}.gcov.json.gz {0}/{0}.gcno {0}/{0} ".format(benchmark))


#

def select_test(benchmark, prioritization, criteria):
    sorted_tests = []
    if (prioritization == 'random'):
        sorted_tests = benchmarks[benchmark]['tests']
        random.shuffle(sorted_tests)
    if (prioritization == 'total_coverage'):
        sorted_tests = sorted(benchmarks[benchmark]['tests'], key=lambda x: len(x[criteria]), reverse=True)
    selected = []
    covered = set()

    if (sorted_tests == None): return selected

    for test in sorted_tests:
        if len(covered) == tot_num[benchmark][criteria]: break
        if (len(covered.union(test[criteria])) == len(covered)): continue
        covered.update(test[criteria])  # add list to set
        selected.append(test['body'])
    return selected


#

def additional_coverage_test_selection(benchmark, criteria):
    universe = set()
    covered = set()
    selected = []
    tests = []

    for test in benchmarks[benchmark]['tests']:
        tests.append(test)
        universe.update(test[criteria])
    #

    while (len(covered) != len(universe)):
        max_test = tests[0]
        max_gap = 0
        residual = universe.difference(covered)
        for test in tests:
            gap = len(residual.intersection(test[criteria]))
            if (gap > max_gap):
                max_test = test
                max_gap = gap
            #
        #

        covered.update(max_test[criteria])
        selected.append(max_test['body'])
        tests.remove(max_test)
    #
    return selected


#

def main():
    for benchmark in directory:
        print(benchmark)
        grip_data(benchmark)
        # random and total coverage
        for prioritization in prioritizations:
            for criteria in criterias:
                selected = select_test(benchmark, prioritization, criteria)

                with open("{0}/{1}_{2}.txt".format(benchmark, prioritization, criteria), "w") as f:
                    for test in selected: f.write(test)
                f.close()
            #
        #
        for criteria in criterias:
            selected = additional_coverage_test_selection(benchmark, criteria)
            with open("{0}/additional_coverage_{1}.txt".format(benchmark, criteria), "w") as f:
                print()
                for test in selected: f.write(test)
            f.close()
    #


#

if __name__ == "__main__":
    main()
#