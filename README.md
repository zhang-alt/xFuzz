# xFuzz
## Quick Start
A container with the dependencies set up can be found [here](https://hub.docker.com/repository/docker/weizhang789/xfuzz).
To open the container, install docker and run:
```
docker push weizhang789/xfuzz:v1 && docker run -it weizhang789/xfuzz bash
```
To evaluate smart contracts in contracts/ inside the container, run:
```
python3 ./static_analysis/main.py && bash fuzzing_script
```
and you are done!

## Installation Instructions

### Solidity Compiler
```
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc
```
### fuzzing engine
refer [here](https://githubmemory.com/repo/duytai/sFuzz).
### static analysis tool
[slither](https://github.com/crytic/slither) and [surya](https://github.com/ConsenSys/surya).

Start fuzzing using the command:
```
python3 ./static_analysis/main.py && bash fuzzing_script
```
