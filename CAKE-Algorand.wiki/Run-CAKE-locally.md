- [Initialize CAKE application](#initialize-cake-application)
- [Message ciphering](#message-ciphering)
- [Access to data](#access-to-data)

### Initialize CAKE application
The databases for all the actors involved in the process need to be created, and then you have to read the keys of the addresses involved and certify on the blockchain the attributes assignment.
To specify the actors you want to give a pair, you have to open 'certification.sh' and use these two lines for each actor involved on the top of the shell script:
```bash
python3 reader_public_key.py --reader 'NAME_OF_THE_ACTOR'
echo "✅ Read public key of NAME_OF_THE_ACTOR"
```
Open the attribute certifier file, 'attribute_certifier.py', and write down the attributes that you intend to give to the actors of the system. 
```python

an_actor_address = config('NAME_OF_THE_ACTOR')
manufacturer_address = config('ADDRESS_MANUFACTURER')
supplier1_address = config('ADDRESS_SUPPLIER1')
supplier2_address = config('ADDRESS_SUPPLIER2')


dict_users = {

    an_actor_address = [str(process_instance_id), 'AN_ATTRIBUTE', 'ANOTHER_ATTRIBUTE'],

    manufacturer_address: [str(process_instance_id), 'MANUFACTURER'],

    supplier1_address: [str(process_instance_id), 'SUPPLIER', 'ELECTRONICS'],

    supplier2_address: [str(process_instance_id), 'SUPPLIER', 'MECHANICS']
}
```
Next, opening 'architecture' directory with you terminal an using the `sh initialize.sh` command you can initialize CAKE.This command creates the necessary databases, resetting the ones already initialized if present, deploys the applications on the Algorand network. In the end, it reads the actors' keys and SKM's keys, and stores the defined attributes in the past step on the blockchain. 

### Message ciphering
Firstly, run the SDM server with `python3 sdm_server.py`. From the terminal you will be able to read what is the address used by the server. Copy and paste it into the .env file, assigning it to the 'SERVER' constant.
```
SERVER = "172.17.0.2"
```
To cipher a message and store it on the blockchain, open the 'data_owner.py' file. Modify the file 'data.json' with the data you want to cipher. Then, modify the access policy and the entries that you need to cipher with a particular policy.

```python
entries = [['ID', 'SortAs', 'GlossTerm'], ['Acronym', 'Abbrev'], ['Specs', 'Dates']]
```
```python
policy = [process_instance_id + ' and (MANUFACTURER or SUPPLIER)',
          process_instance_id + ' and (MANUFACTURER or (SUPPLIER and ELECTRONICS))',
          process_instance_id + ' and (MANUFACTURER or (SUPPLIER and MECHANICS))']
```

The message to be encrypted must be saved in the path 'CAKE-Algorand/architecture/file/data.json'. The following example is an instance of a message to be encrypted.

```json
{
    "ID": "SGML",
    "SortAs": "LMGS",
    "GlossTerm": "Standard Generalized Markup Language",
    "Acronym": "GSML",
    "Abbrev": "ISO 8879:1986",
    "Specs": "928162",
    "Dates": "NOW"
}
```

Then run `sh data_owner.sh` to make an handshake an a ciphering request. It is also possible to split these two actions running `python3 data_owner.py -hs` to perform the handshake and `python3 data_owner.py -c` to cipher.
+At this point,the SDM Server will print the 'slice_id' and 'message_id' values,these information will be used for the key request phase.
```
[STARTING] server is starting...
[LISTENING] Server is listening on 172.17.0.2
[NEW CONNECTION] ('172.17.0.2', 58680) connected.
[ACTIVE CONNECTIONS] 1
Handshake successful
slice id: 11405747102899531556
slice id: 3622467048620169296
slice id: 8386550832079592906
message id: 6389222717092303342
ipfs hash: QmXoat6pFTVWqahzXvCQTgQ37y7GjUjCBikqFe2cYGUyCi
```
### Access to data

To send a request via SSL, open the 'client.sh' file, specify the constants like 'reader_address', 'message_id' and 'slice_id, then run ```python3 skm_server.py```. Then, run ```sh client.sh```. This command makes an handshake between the reader and the skm_server, it requests a decryption key and, finally, accesses the data.
If the policy allows it, you will read the data you requested on the terminal.
If the address used has already performed a handshake and a key generation request, it will be necessary to use ```sh client.sh``` setting the variables in the same way.