set -e
echo "Deploying AttributeCertifierContract"
python3.10 blockchain/AttributeCertifierContract/AttributeCertifierContractMain.py -d
echo "Deployed AttributeCertifierContract"
echo "Deploying MessageContract"
python3.10 blockchain/MessageContract/MessageContractMain.py -d
echo "Deployed MessageContract"
echo "Deploying PKSKMContractMain"
python3.10 blockchain/PublicKeySKM/PKSKMContractMain.py -d
echo "Deployed PKSKMContractMain"
echo "Deploying PKReadersContractMain"
python3.10 blockchain/PublicKeysReadersContract/PKReadersContractMain.py -d
echo "Deployed PKReadersContractMain"