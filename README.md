# Fine-grained Data Access Control for Collaborative Process Execution on Blockchain

This repository contains the **Algorand**-based version of the CAKE approach presented in the paper "[Fine-grained Data Access Control for
Collaborative Process Execution on Blockchain](https://arxiv.org/abs/2207.08484)" (DOI: [10.1007/978-3-031-16168-1_4](https://doi.org/10.1007/978-3-031-16168-1_4); slides are available on [SlideShare](https://www.slideshare.net/EdoardoMarangone/finegrained-data-access-control-for-collaborative-process-execution-on-blockchain-253133788)). Please find and fork the latest release based on **Ethereum** at [github.com/apwbs/CAKE-Ethereum](https://github.com/apwbs/CAKE-Ethereum/)!

In this [Docker Hub repository](https://hub.docker.com/repository/docker/apwbs/cake/general) there are the two Docker Images 
for the Ethereum and Algorand implementation of the CAKE approach.

## Guide
 
### Docker execution
There are two ways to run the system. The first one is to download the corresponding Docker Image for the Algorand implementation stored at the [Docker Hub](https://hub.docker.com/repository/docker/apwbs/cake/general).

Otherwise, it is (strongly) recommended to install Docker and create a new image running Ubuntu 18.04 and then start one
or more containers from that image. To do this, firstly use the DockerFile running `docker build -t image_name PATH_TO_THE_DOCKERFILE/DockerFiles/`
to create a docker image. Then run `docker run -it -v PATH_TO_CAKE-AlgorandFOLDER/CAKE-Agorand/:/CAKE-Algorand image_name`
to create a container starting from the image created in the previous step. To run the first instance of a container run
`docker start container_name`, then run `docker attach container_name`. To run other independent instances of the same container run
`docker exec -it container_name bin/bash`. Running other instances (from the second on) of the same container with 
`docker start` and `docker attach` will not make them independent. Every command in one instance will be applied also in the
other instances. Using `docker exec` you can open as many independent containers as you like.

### Set enviroments
Before deploying the contracts it is necessary to create the private and public keys necessary for the process in the .`env` file, together with the network access TOKEN information.
Open .env with an editor and save your ALGOD_TOKEN and ALGOD_ADDRESS using this syntax:
```python
ALGOD_TOKEN = '2HrTwfGLLo3Ly5jqxsI7LhQ4iui1EPt7m7NVc7Bb'
ALGOD_ADDRESS = 'https://testnet-algorand.api.purestake.io/ps2'
```
Then, you have to generate the keys you need, you can proceed running `python3 account_creation.py -a` in '\CAKE-Algorand', in this way your `.env` file will be populad. Be careful because this operation can lead to the deletion of any private and public keys saved in the `.env` if it is already populed. Alternatively, you can proceed generating keys and copying manually then in `.env` build a file like in the example. To do this you have to run `python3 account_creation.py` in \CAKE-Algorand.

At the end of this phase the file .env should contains these content

```python
ALGOD_TOKEN = '2HrTwpGLLo3Ty5jqxsI2LhQ4aua1EPt1m2NVc4Bb'
ALGOD_ADDRESS = 'https://testnet-algorand.api.purestake.io/ps2'

ADDRESS_CERTIFIER = 'T4PMAA6ODUO3OUAKMG5SFMKYYYSZZIITXReFEXWMIEE2ED2ZIVWHNFG62Q'
CERTIFIER_PRIVATEKEY = 'YKOWBfu7iNNPGXMSgR3jBC+BAd34Ih6RixyX9Ms7pZOjefHsADzh5dt1AKYbsisVjGJZyhE7xMUl7MQQmiD1lFbA=='
ADDRESS_MANUFACTURER = 'S4HU4ZINJ5YHL2OBW3VM6S5HLKRSRR2XWPVDFMHGEKR5TVHV2VOFLOEWGE'
PRIVATEKEY_MANUFACTURER = 'nmSjXkuXkHKeqTLq040L2dHcqjL4wmNNT+2ZfFjOm71XD05lDU9wdenBturPS6daoyjHV7PqMrDmIqPZ1PXVXA=='
ADDRESS_SUPPLIER1 = 'MEDEZGMMSDFUBBWSMVDNN3HGL44SS7OPIDAC4H6SMPRWRBAXIM2SHEN3Z4'
PRIVATEKEY_SUPPLIER1 = 'bhCjuETdIGXn8FBrx4rg3fPez0CGOVBlbDPVJl1v560hBkyZjJDLQIbSZUbW7OZfOSl9z0DALh/SY+NohBdDNQ=='
ADDRESS_SUPPLIER2 = 'F3BSOBNOWCOO7SPNNKWWE3LHTJ2A47CLPJXXLAJ2W5IQVG5HK2GZB56AWQ'
PRIVATEKEY_SUPPLIER2 = '8c1d0nreo+yKS6JRxTioY5729mbYnTno7LmjN+n/cCguwycFrrCc78ntaq1ibWeadA58S3pvdYE6t1EKm6dWjQ=='
SKM_ADDRESS = 'RBA7GTS7RGTQWET7E7RBR5VRG5ZQCL5E64FTTTGQ7KE2BJRE7TURWWG424'
SKM_PRIVATEKEY = 'jw0LpXEhtedkzgsp1TfxEctGZEFJFzKTTkUu1bdlYTCIQfNOX4mnCxJ/J+IY9rE3cwEv1PcLOczQ+omgpiT86Q=='
SDM_ADDRESS =  'WIEBSFRLYXWE6CXYRMD2762SNQV4SWUBYI3TH4ZL3NKKVHWMT7IF5R2N3A'
SDM_PRIVATEKEY = 'z98uZ1GxnGEITm+HuzX2HsqGxEZBCpgKnBHJJnrUSeayCBkWK8XsTwr3iwev+1JsK+lagcI3M/Mr21Sqnsyf0A=='s
ADDRESS_CREATOR = 'PQMOY2OEGP77TSJSBJRMKHRYA2YS34GOFJMH2LVYMPVPPLQZJZNBJSTX74'
CREATOR_PRIVATEKEY =  '3rLhwfN9Z+GkYuXSpHTd51JW1CN+eS0NwI/FriwBMGN8GOxpxDP/+ckyCmLFHjgGsS3wzipYfS32Y+r3rhlOWg=='
PASSPHRASE_CREATOR = 'forward girl thought soccer solve debate benefit vulcano olympic spoon upgrade common protect vital valve just pizza ability side unable sun about book about that'
```

At the end of these phase you have to use and Algo Dispenser [like this](https://bank.testnet.algorand.network/) to get some Algo for each of your new addresses.

### Inizialize CAKE application
Open the attribute certifier file, 'attribute_certifier.py', and write down the attributes that you intend to give to the actors of the system. 
```python
    dict_users = {
        manufacturer_address: [str(process_instance_id), 'MANUFACTURER'],

        supplier1_address: [str(process_instance_id), 'SUPPLIER', 'ELECTRONICS'],

        supplier2_address: [str(process_instance_id), 'SUPPLIER', 'MECHANICS']
    }
```
Next, opening 'architecture' directory with you terminal an using the `sh initialize.sh` command you can initialize CAKE.This command creates the necessary databases, resetting the ones already initialized if present, deploys the applications on the Algorand network. In the end, it read the actors' keys and skm's keys, and store the defined attributes in the past step on the blockchain. 

### Message ciphering and delivering
Firstly, run the SDM server with `python3 sdm_server.py`. To cipher a message and store it on the blockchain, open the 'data_owner.py' file. Modify the file 'data.json' with the data you want to cipher. Then, modify the access policy and the entries that you need to cipher with a particular policy.

```python
entries = [['ID', 'SortAs', 'GlossTerm'], ['Acronym', 'Abbrev'], ['Specs', 'Dates']]
```
```python
policy = [process_instance_id + ' and (MANUFACTURER or SUPPLIER)',
          process_instance_id + ' and (MANUFACTURER or (SUPPLIER and ELECTRONICS))',
          process_instance_id + ' and (MANUFACTURER or (SUPPLIER and MECHANICS))']
```

The message to be encrypted must be saved in the path 'CAKE-Algorand/architecture/file/data.json'. The following example is an instance of a cipherable message.

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

The run `sh data_owner.py` to make an handshake an a ciphering request. It's also possible to split these two action running `python3 data_owner.py -hs` to handshake and `python3 data_owner.py -c` to cipher.
At this point,the SDM Server will print the 'slice_id' and 'message_id' values, these information will be used to key requesting.
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

To send a request via SSL, open the 'client.sh' file, specify the constants like 'reader_address', 'message_id' and 'slice_id, then run ```python3 skm_server.py```. Then, run ```sh client.py```. This command make an handshake between the reader and the skm_server, then it request a key generation and in the end it use to access to the data.
If the policy allows it, you will read the data you requested on the terminal.
If the address used has already performed a handshake and a key generation request, it will be necessary to use ```sh client.py``` setting the variables in the same way.

## API Guide
CAKE also has an API to manage its interaction, this section describes its structure and use.

### Requirement
To use the api you need to install flask, open the terminal and run `pip install flask`.
To interract with the API you need to user requests library. So your python script have to import it.  
```python
    import requests 

    #YOUR CODE
```
### Initizialization
The database resetting and the deployment of the contract cannot be done using the API, you have to open your terminal and run in 'CAKE-Algorand/architecture' `sh resetDB.sh` and `sh deploy.sh`. At this point is possible to lunch the API, running `python3 API/api.py`.

The terminal will show the base path to use to interract the API (in the following example it is 'http://127.0.0.1:8888/')

```
root@7e473ad21d74:/CAKE-Algorand/architecture# python3 API/api.py 
 * Serving Flask app 'api' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8888/ (Press CTRL+C to quit)
```

At this point the API is running, an it's possible interract with it.
To test if api is correctly working you can run this script anche check if the request status is 200.

```python
    import requests

    response = requests.get('http://127.0.0.1:8888/')
```

### Read keys and attribute certification

Using the API it is possible to read the keys of the skm server actors, and assign the desired roles to the actors involved.
It is necessary to define a list with the names of the actors, remember that the name must be the same used inside the env when the address and public key of the actor are specified.
In addition to a list of strings with the actors involved, a dictionary must be defined that associates the roles assigned to the actors involved. Each actor can have multiple roles, and each role can be assigned multiple times.
These two data structures will have to be inserted in a dictionary, with 'actors' and 'roles' as keys respectively, and given as input as in the following example during the request to the api server.

```python
    import requests 

    actors = ['MANUFACTURER', 'SUPPLIER1', 'SUPPLIER2']
    roles = {'MANUFACTURER': ['MANUFACTURER'],
        'SUPPLIER1': ['SUPPLIER', 'ELECTRONICS'],
        'SUPPLIER2': ['SUPPLIER', 'MECHANICS']}

    input = {'actors': actors, 'roles': roles}

    response = requests.post('http://127.0.0.1:8888/certification', json = input)

```
This method return as response the process, to access to this value you can use `response.text`. This value has to be stored on the .env.
At the end of this run, you have to lunch the SDM and SKM servers using `python3 sdm_server.py` and `python3 skm_server.py`.

This request can be splitted in the following three differents request to the api server, like in the following three subsections. For a correct functioning it is necessary to carry out these operations in the proposed order.

#### Read public key

Using the method in the example is possible to ask to server to read the keys of the actors stored in the '.env' files.
It is necessary to construct a list with the names of the actors, and then a insert the list into a dictionary with the key 'actors', like to what was described previously. This dictionary will be input like in the example.
```python
    import requests 

    actors = ['MANUFACTURER', 'SUPPLIER1', 'SUPPLIER2']

    input = {'actors': actors}

    response = requests.post('http://127.0.0.1:8888/certification/readpublickey',
        json = input)

```

#### Read SKM's key

Using the method in the example is possible to ask to server to read the key of the SKM server stored in the '.env'.
This method doen't need any input.

```python
    import requests 

    response = requests.post('http://127.0.0.1:8888/certification/skmpublickey')

```

#### Attribute certification

This method allows you to certify on the blockchain the roles assigned to the actors, whose key has previously been read. A dictionary must be defined that associates the roles assigned to the actors involved. Each actor can have multiple roles, and each role can be assigned multiple times.
This dictonary will have to be inserted in a dictionary, with 'roles' as key, and given as input as in the following example during the request to the api server.

```python
    import requests 

    roles = {'MANUFACTURER': ['MANUFACTURER'],
        'SUPPLIER1': ['SUPPLIER', 'ELECTRONICS'],
         'SUPPLIER2': ['SUPPLIER', 'MECHANICS']}

    input = {'roles': roles}

    response = requests.post('http://127.0.0.1:8888/certification/attributecertification',
        json = input)

```

This method return as response the process, to access to this value you can use `response.text`. This value has to be stored on the .env.
At the end of this run, you have to lunch the SDM and SKM servers using `python3 sdm_server.py` and `python3 skm_server.py`.

### Interraction with SDM 

The python script described in this section allows to send message to the SDM server using the API, allowing to cipher a message.
The following example is an instance of a cipherable message

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

#### Handshake
To make an handshake it's necessary to build a dictionary with the process instance id corrisponding to the key 'process_id', and to send a post request to 'dataOwner/handshake'.
Note that the process instance id is the only value that will be input from here on using as `int`.

```python
    import requests 

    process_instance_id = 1234567890 #Process id generated after the attribute certification
    
    input = {'process_id' : process_instance_id}

    response = requests.post('http://127.0.0.1:8888/dataOwner/handshake',
        json = input)
```

#### Cipher
If the handshaking operation is completed correctly, you can proceed with the encryption of the message.
You have to build a dictionary, with the described information associated with the following keys:
- `'processe_id'` : the process_id showed at the end of attribute certification
- `'entries'` : a list in which each element is a group of entries of the message to be encrypted which will be associated with the same privacy. These groups are represented by a list of strings, where the strings are associated with the keys of the json file.
- `'policy'` : a string list containing the process_id and the specific policy for the group of entries with the same index in the 'entries' vector. The correct formatting can be seen in the next code example.
- `'message'` : a string generated from reading the json file containg the messago to cipher

```python
    import requests 

    process_instance_id = 1234567890 #Process id generated after the attribute certification
    
    entries = [['ID', 'SortAs', 'GlossTerm'],
        ['Acronym', 'Abbrev'],
        ['Specs', 'Dates', 'GlossTerm']]

    policy = [process_instance_id + ' and (MANUFACTURER or SUPPLIER)',
          process_instance_id + ' and (MANUFACTURER or (SUPPLIER and ELECTRONICS))',
          process_instance_id + ' and (MANUFACTURER or (SUPPLIER and MECHANICS))']

    g = open('your/data.json')

    message_to_send = g.read()

    input = {'process_id': process_instance_id,
        'entries': entries,
        'policy' : policy, 
        'message': message_to_send}

    response = requests.post('http://127.0.0.1:8888/dataOwner/cipher',
        json = input)
```
At the end of this operation it is important to take note of the slice_id and message_id values generated and displayed on the terminal where the sdm server runs.

```
[ACTIVE CONNECTIONS] 1
Handshake successful
slice id: 5375500895703771247
slice id: 17604598720062938551
slice id: 10338915769088273764
message id: 13846106420650213324
```

The slice_id values represent the groups of labels defined in entries, while the message_id is an identifier of the encrypted message.

### Interraction with SKM
This section describes the methods that allow you to interact with the SKM Server, allowing you to make a handshake with the actors, generate a key and have access to encrypted messages.
#### Handshake

Also this time a handshaking is necessary, therefore it is necessary to indicate the address of the reader inside the dictionary given in input using the key 'reader address'. It is also necessary to enter the ID of the message to be decrypted using 'message_id' as key, and the process_id as in the previous step.

```python
    import requests 

    process_instance_id = 1234567890 #Process id generated after the attribute certification
    message_id = '13846106420650213324' 
    reader_address = 'N2C374IRX7HEX2YEQWJBTRSVRHRUV4ZSF76S54WV4COTHRUNYRCI47R3WU'

    input = {'process_id' : process_instance_id,
        'message_id': message_id,
        'reader_address' : reader_address}

    response = requests.post('http://127.0.0.1:8888/client/handshake',
        json = input)

```

#### Generate Keys

At this point using the same dictionary of the previous step it is possible to generate a key for the reader.

```python
    import requests 

    process_instance_id = 1234567890 #Process id generated after the attribute certification
    message_id = '456'
    reader_address = 'N2C374IRX7HEX2YEQWJBTRSVRHRUV4ZSF76S54WV4COTHRUNYRCI47R3WU'

    input = {'process_id' : process_instance_id,
        'message_id': message_id,
        'reader_address' : reader_address}

    response = requests.post('http://127.0.0.1:8888/client/generateKey',
        json = input)

```

#### Access Data

By adding the value of the slice id corresponding to the portion of the message to be decrypted to the previously defined dictionary, it is finally possible to access it.

```python
    import requests 

    process_instance_id = 1234567890 #Process id generated after the attribute certification
    slice_id = '123'
    message_id = '456'
    reader_address = 'N2C374IRX7HEX2YEQWJBTRSVRHRUV4ZSF76S54WV4COTHRUNYRCI47R3WU'

    input = {'process_id' : process_instance_id,
        'slice_id' : slice_id,
        'message_id': message_id,
        'reader_address' : reader_address}

    response = requests.post('http://127.0.0.1:8888/client/accessData',
        json = input)

```