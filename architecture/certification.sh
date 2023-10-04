# Read public key of manufacter and suppliers
set -e
python3 reader_public_key.py --reader 'MANUFACTURER'
echo "✅ Read public key of MANUFACTURER"
python3 reader_public_key.py --reader 'SUPPLIER1'
echo "✅ Read public key of SUPPLIER1"
python3 reader_public_key.py --reader 'SUPPLIER2'
echo "✅ Read public key of SUPPLIER2"

python3 skm_public_key.py
echo "✅ Read public key of skm"

python3 attribute_certifier.py 
echo "✅ Attribute certifier done"