import json
from solcx import compile_standard, install_solc
install_solc("0.7.0")

with open("./ChallengeContract.sol", "r") as file:
    challenge_contract_file = file.read()

# Compile
compiled_sol = compile_standard(
    {
        'language': 'Solidity',
        'sources': {'ChallengeContract.sol': {'content': challenge_contract_file }},
        'settings' : {
            'outputSelection' : {
                '*' : {'*' : ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']}
            }
        },
    },
    solc_version='0.7.0'
)

with open('compiled_code.json', 'w') as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol['contracts']['ChallengeContract.sol']['ChallengeContract']['evm'][
 'bytecode'
]['object']

# get abi
abi = compiled_sol['contracts']['ChallengeContract.sol']['ChallengeContract']['abi']