import gzip
import json
import os
import re
import subprocess
from subprocess import PIPE
from subprocess import STDOUT
import random

root = "backup/"
__debug__ 

directory=['printtokens2','printtokens','replace','schedule','schedule2','tcas','totinfo']
prioritizations=['random', 'total_coverage', 'additional_coverage']
criterias=['statements','branches']
benchmarks={}
tot_num = {}

#test corresponding version on test suite test_suite
def test_version(benchmark, test_suite, version):
    output = ""
    if(benchmark == "replace" or benchmark == "totinfo"):
        os.system("cd {0}/{1} && gcc -Wno-return-type -w -g -o {0} {0}.c -lm".format(benchmark,version))
        os.system("cd {0} && gcc -Wno-return-type -w -g -o {0} {0}.c -lm".format(benchmark))
    else:
        os.system("cd {0}/{1} && gcc -Wno-return-type -w -g -o {0} {0}.c ".format(benchmark,version))
        os.system("cd {0} && gcc -Wno-return-type -w -g -o {0} {0}.c ".format(benchmark))
    #
    with open(benchmark+"/"+test_suite+".txt", "r") as f:
        tests = f.readlines()
        line_num = 0
        false_num = 0
        for test in tests:
            line_num+=1
            #print(line_num)
            #print("cd {0} && ./{0} {1}".format(benchmark,test))
            #print("cd {0} && ./{1}/{0} {2}".format(benchmark,version,test))
            p_origin = subprocess.Popen("cd {0} && ./{0} {1}".format(benchmark,test), stdout=PIPE, stderr=STDOUT, shell=True)
            p_version = subprocess.Popen("cd {0} && ./{1}/{0} {2}".format(benchmark,version,test), stdout=PIPE, stderr=STDOUT, shell=True)
            real = p_origin.stdout.read()
            actual = p_version.stdout.read()
            rc1 = p_origin.wait()
            rc2 = p_version.wait()
            if(real!=actual):
                output += test
                false_num +=1
        #
    #
    #print(line_num)
    #print(false_num)
    if __debug__: print("suite_size: "+str(line_num)+"\tfalse_num: "+str(false_num))
    f.close()
    return output
#

def main():
    for benchmark in directory:
        if not os.path.exists("{0}/{1}".format(benchmark,"outputs")):os.system("mkdir {0}/{1}".format(benchmark,"outputs"))
        if not os.path.exists("{0}/{1}/{2}".format(benchmark,"outputs","universe")):os.system("mkdir {0}/{1}/{2}".format(benchmark,"outputs","universe"))
        
        ind = 1
        while(os.path.exists("{0}/v{1}".format(benchmark,ind))):
            if __debug__: print(benchmark+"_"+"universe_v"+str(ind))
            vi_result = test_version(benchmark, "universe", "v"+str(ind))
            with open("{0}/{1}/{2}/{3}.txt".format(benchmark,"outputs","universe","v"+str(ind)), "w") as f:
                f.write(vi_result)
            f.close()
            ind+=1
        #
        
        for prioritization in prioritizations:
            for criteria in criterias:
                test_suite = prioritization+"_"+criteria
                #print(test_suite)
                if not os.path.exists("{0}/{1}/{2}".format(benchmark,"outputs",test_suite)):os.system("mkdir {0}/{1}/{2}".format(benchmark,"outputs",test_suite))
                ind = 1
                while  (os.path.exists("{0}/v{1}".format(benchmark,ind))):
                    if __debug__: print(benchmark+"_"+test_suite+"_v"+str(ind))
                    vi_result = test_version(benchmark, test_suite, "v"+str(ind))
                    with open("{0}/{1}/{2}/{3}.txt".format(benchmark,"outputs",test_suite,"v"+str(ind)), "w") as f:
                        f.write(vi_result)
                    f.close()
                    ind+=1
                #
            #
        #
                
    #
#

if __name__ == "__main__":
    main()
#