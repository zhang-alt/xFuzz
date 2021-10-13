import os
import copy
import sys

# get the midlevel files
def get_public_function_from_sol(dir, suffix):
    res = []
    for root, directory, files in os.walk(dir):
        for filename in files:
            name, suf = os.path.splitext(filename)
            if suf == suffix:
                find = os.path.join(root, filename)
                # "slither --disable-color  --detect tx-origin ./ReentrancyAttacker.sol"
                if filename.startswith('test') or filename.startswith('0x'):
                    # print("slither --disable-color  --detect tx-origin " + find)
                # ' > ./mid_files/' + name + '.res')
                # os.system("slither " + find + ' > ./mid_files/' + name + '.res' )
                    os.system("surya describe " + find + ' > ./mid_files/' + filename.replace('.sol', '.txt'))
                # "surya describe examples/printers/call_graph.sol"
                # os.system("python3 merge.py ")
                res.append(find)
    return res

def get_call_graph_from_sol(dir, suffix):
    res = []
    for root, directory, files in os.walk(dir):
        os.chdir('./mid_files')
        for filename in files:
            name, suf = os.path.splitext(filename)
            if suf == suffix:
                find = os.path.join('../contracts', filename)
                os.system("slither " + find + ' --print call-graph')
                os.system('cp all_contracts.dot ' + filename.replace('.sol', '.dot'))
                res.append(find)
    os.chdir('..')
    return res


def compile_all_sol(dir, suffix):
    res = []
    compile_template = "solc --combined-json abi,bin,bin-runtime,srcmap,srcmap-runtime,ast contracts/e2.sol > contracts/e2.sol.json"
    for root, directory, files in os.walk(dir):
        for filename in files:
            name, suf = os.path.splitext(filename)
            if suf == suffix:
                # find = os.path.join('./contracts', filename)
                get_compile_command = compile_template.replace('e2.sol', filename)
                os.system(get_compile_command)
                # res.append(find)
    return res



def static_analysis_phase():
    get_public_function_from_sol("./contracts", '.sol')
    get_call_graph_from_sol("./contracts", '.sol')
    compile_all_sol("./contracts", '.sol')




