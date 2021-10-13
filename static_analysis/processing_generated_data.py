import os
import copy
import sys
import re
defaultencoding = 'utf-8'
sys.setrecursionlimit(10000)

a_single_path = []
all_paths_in_cfg = []
DFS_has_contained = set()
ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

def dfs(graph, start):
    if start not in DFS_has_contained:
        DFS_has_contained.add(start)
        a_single_path.append(start)
    if start not in graph:
        all_paths_in_cfg.append(copy.deepcopy(a_single_path))
        a_single_path.pop()
        return
    for node in graph[start]:
        if node not in DFS_has_contained:
            dfs(graph, node)
    a_single_path.pop()

def deal_call_paths(fileName):
    graph = dict()
    notFirst = set()
    global a_single_path
    global all_paths_in_cfg
    all_paths_in_cfg = []
    a_single_path = []
    mp = dict()

    f = open(fileName, 'r')
    lines = f.readlines()
    lastLine = False
    for line in lines:
        if line.find('subgraph cluster_') >= 0:
            id = line.split('_')[1]
            continue
        if line.startswith('label = "'):
            contract = line.split()[-1].replace('\"', '')
            if contract != '[Solidity]':
                mp[id] = contract
            continue

        if line.startswith('}"'):
            lastLine = True
            line = line.replace('}', '')
        if True and line.startswith('\"') and line.find('->') > 0:
            fir_sec = line.replace('\"', '').replace('\n', '').replace(' ', '').split('->')
            if fir_sec[0][0].isalnum():
                con, fun = fir_sec[0].split('_', 1)
                st = mp[con] + ':' + fun
                if fir_sec[1][0].isalnum():
                    con, fun = fir_sec[1].split('_', 1)
                    en = mp[con] + ':' + fun
                    notFirst.add(en)
                    if st in graph:
                        graph[st].append(en)
                    else:
                        graph[st] = [en]

    for key in graph:
        if key not in notFirst and len(graph[key]) > 0:
            global DFS_has_contained
            DFS_has_contained = set()
            a_single_path = []
            dfs(graph, key)

def deal(fileName):
    fo = open(fileName, 'r')
    lines2 = fo.readlines()
    preIsEndl = False
    start = False
    graph = dict()
    notFirst = set()
    global a_single_path
    global all_paths_in_cfg
    all_paths_in_cfg = []
    a_single_path = []

    for line in lines2:
        if preIsEndl and len(line) > 2 and line[2] == '\"':
            start = True
        if start and len(line) <= 2:
            end = True
            break
        if start:
            if line.find('->') > 0:
                edge = line.split('[')[0]
                two = edge.replace('\"', '').split(' ')
                begin = two[2]
                end = two[-2]
                if end == '->':
                    continue
                notFirst.add(end)
                if begin in graph:
                    graph[begin].append(end)
                else:
                    graph[begin] = [end]
            else:
                node = line.replace(' ', '').replace('\"', '').split(';')[0]
                graph[node] = []

        if len(line) <= 1:
            preIsEndl = True
        else:
            preIsEndl = False

    for key in graph:
        if key not in notFirst and len(graph[key]) > 0:
            global DFS_has_contained
            DFS_has_contained = set()
            a_single_path = []
            dfs(graph, key)


mp = dict()
all_funs = set()

def deal_public_function(fileName):
    fo = open(fileName, 'r')
    lines = fo.readlines()
    # this variable is used to indicate whether it's a contract
    isAble = False
    contractName = ''
    # public function in contract
    global mp
    mp = dict()
    global all_funs
    all_funs = set()
    for line in lines:
        line = ansi_escape.sub('', line)
        # end a contract analysis
        if len(line) <= 1:
            isAble = False
            if len(contractName) > 0:
                mp[contractName] = funs
            continue
        # start a contract analysis
        if not isAble:
            if line.find('+') >= 0 and line.find('[Lib]') < 0:
                isAble = True

                contractName = line.split()[1]
                funs = []
                continue
        # judge function
        if isAble:
            if line.find('[Pub]') >= 0 or line.find('[Ext]') >= 0:
                funName = line.split()[2]
                # print(line.split())
                funs.append(funName)
                all_funs.add(funName)
                continue

spath = []

def simplify_chain(fin):
    global spath
    spath = []
    for chain in all_paths_in_cfg:
        little_long = []
        for node in chain:
            contract, fun = node.split(':', 1)
            # It is a public function in a contract
            if contract in mp and fun in all_funs:
                little_long.append([contract, fun])
        more_short = []
        for i in range(1, len(little_long)):
            if little_long[i - 1][0] == little_long[i][0]:
                continue;
            else:
                more_short = little_long[i - 1:]
                break

        if len(more_short) > 1:
            spath.append(more_short)
            # print(more_short)
            for m in more_short:
                fin.write(m[0] + ':' + m[1] + '->')
            fin.write('\n')


# deal midlevel files
def generate_call_chain(dir, suffix, fin):
    res = []
    for root, directory, files in os.walk(dir):
        for filename in files:
            name, suf = os.path.splitext(filename)
            if suf == suffix:
                fin.write("#file " + name + '.sol\n')
                find = os.path.join(root, filename)
                deal_call_paths(find)
                if name + '.txt' in files:
                    # print(find.replace('.dot', '.txt'))
                    deal_public_function(find.replace('.dot', '.txt'))
                else:
                    continue
                simplify_chain(fin)
                res.append(find)
    fin.close()
    return res

# ---------------------------------------------------------------
# produce commands
call_chain_template = "fuzzer --file ./contracts/CoinolixToken.sol.json --source ./contracts/CoinolixToken.sol --name  --function  --externalcall  --assets assets/ --duration 240 --mode 0 --reporter 0 --attacker ReentrancyAttacker"

single_function_template = "fuzzer --file ./contracts/CoinolixToken.sol.json --source ./contracts/CoinolixToken.sol --name --function  --assets assets/ --duration 180 --mode 0 --reporter 0 --attacker ReentrancyAttacker "
contracts = set()
per_len = dict()
chains=set()
sinCon = set()
fw=open('fuzzing_script','w')

def produce_fuzzing_script(fileName):
    count = 0
    fo = open(fileName, 'r')
    lines = fo.readlines()

    for line in lines:
        if line.startswith('#file'):
            file = line.split()[1]
            f_t = set()
        elif file+line not in chains:
            count+=1
            # print(count)
            cons = line.replace('\n', '').replace(' ', '').split('->')
            cons = cons[:-1]
            # print(cons)
            chains.add(file+line)

            td = set()
            for node in cons:
                td.add(node.split(':')[0])
                if file+node not in sinCon:
                    sinCon.add(file+node)
                    an = single_function_template.replace('CoinolixToken.sol', file).replace('--name ',
                                                                        ' --name ' + node.split(':')[0]).replace(
                        '--function ', '  --function ' + node.split(':')[1])
                    fw.write(an+'\n')


            if len(td) in per_len:
                per_len[ len(td)]+=1
            else:
                per_len[len(td)] = 1

            for i in range(0, len(cons) - 1):
                # external call
                ext = cons[i].replace(':', '_')
                # 目标函数
                tar= cons[i + 1].split(':')
                same = cons[i].split(':')[0] == tar[0]
                if not same and cons[i]+cons[i + 1] not in f_t :
                    f_t.add(cons[i]+cons[i + 1])
                    contracts.add(tar[0])
                    contracts.add(cons[i].split(':')[0])
                    na = call_chain_template.replace('CoinolixToken.sol', file).replace('--name ', '--name ' + tar[0]).replace(
                        '--function ', '--function ' + tar[1]).replace('--externalcall ', '--externalcall ' + ext)
                    fw.write(na+'\n')
                    # print(na)

def processing_generated_data():
    file_name = "./callchain.txt"
    fin = open(file_name, "w")
    generate_call_chain("./mid_files", '.dot', fin)
    produce_fuzzing_script(file_name)
    fw.flush()
    fw.close()
    
    













