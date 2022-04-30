# xFuzz
## Quick Start
A container with the dependencies set up can be found [here](https://hub.docker.com/repository/docker/weizhang789/xfuzz).
To open the container, install docker and run:
```
docker push weizhang789/xfuzz:v1 && docker run -it weizhang789/xfuzz:v1 bash
```
To evaluate smart contracts in contracts/ inside the container, run:
```
python3 ./static_analysis/main.py && bash fuzzing_script
```
and you are done!

## Installation Instructions

### Solidity Compiler
```
pip install solc-select
solc-select install 0.4.26
solc-select use 0.4.26
```
### fuzzing engine
Refer sfuzz installation, [here](https://githubmemory.com/repo/duytai/sFuzz).
### static analysis tool
We also need the static analysis tools, [slither](https://github.com/crytic/slither) and [surya](https://github.com/ConsenSys/surya).

### fuzzing tests
Start fuzzing a folder(e.g., "/contracts"), using the command:
```
python3 ./static_analysis/main.py && bash fuzzing_script
```
Start fuzzing the specified smart contracts, using the command:
```
solc --combined-json abi,bin,bin-runtime,srcmap,srcmap-runtime,ast SOL_FILE > SOL.json

fuzzer --file SOL.json --source SOL_FILE  --name CONTRACT  --function FUNCTION  --externalcall CONTRACT_FUNCTION --assets assets/ --duration 300 --mode 0 --reporter 0 --attacker ReentrancyAttacker
```


