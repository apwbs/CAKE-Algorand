set -e
cd blockchain

cd AttributeCertifierContract
echo "Deploying AttributeCertifierContract"
python3.10 AttributeCertifierContractMain.py -d
#python3.10 blockchain/AttributeCertifierContract/AttributeCertifierContractMain.py -d
echo "Deployed AttributeCertifierContract \n"

cd ../MessageContract
echo "Deploying MessageContract"
python3.10 MessageContractMain.py -d
#python3.10 blockchain/MessageContract/MessageContractMain.py -d
echo "Deployed MessageContract \n"

cd ../PublicKeySKM
echo "Deploying PKSKMContractMain"
python3.10 PKSKMContractMain.py -d
#python3.10 blockchain/PublicKeySKM/PKSKMContractMain.py -d
echo "Deployed PKSKMContractMain \n"

cd ../PublicKeysReadersContract
echo "Deploying PKReadersContractMain"
python3.10 PKReadersContractMain.py -d
#python3.10 blockchain/PublicKeysReadersContract/PKReadersContractMain.py -d
echo "Deployed PKReadersContractMain"