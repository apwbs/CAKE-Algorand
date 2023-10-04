1. [POST /dataOwner/handshake](#post-dataownerhandshake)
2. [POST /dataOwner/cipher](#post-dataownercipher)

## POST /dataOwner/handshake

This method is used to make an handshake between the data owner and the SDM Server. It requires the process instance id as parameter.

### Request Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| process_id | int | Yes | The ID of the process instance |

### Response Parameters
| Name | Type | Description |
|------|------|-------------|
| status | int | The status code of the response (200 if successful) |

### Example Request

```python
import requests

process_instance_id = 314159265 

input = {'process_id' : process_instance_id}

response = requests.post('http://127.0.0.1:8888/dataOwner/handshake',
    json = input)
```

## POST /dataOwner/cipher

This method is used to send the ciphered data to the SDM Server. It requires the process instance id, the message to cipher, the policy of the messages and the entries of the policy.

### Request Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| process_id | int | Yes | The ID of the process instance |
| message | str | Yes | A string generated from reading the json file containing the message to cipher |
| policy | str | Yes | A list of strings containing a logical expression for each group of entries. In the logical expression it is possible to specify the associated process instance id and the roles of who has the right to read the associated entry. The correct formatting can be seen in the next code example | 
+| entries | str | Yes | A list in which each element is a group of entries of the message to be encrypted which will be associated with the same privacy. These groups are represented by a list of strings, where the strings are associated with the keys of the json file |
 
### Response Parameters
| Name | Type | Description |
|------|------|-------------|
| status | int | The status code of the response (200 if successful) |

### Example Request

```python
import requests 

    process_instance_id = 314159265 #Process id generated after the attribute certification
    
    entries = [['ID', 'SortAs', 'GlossTerm'],
        ['Acronym', 'Abbrev'],
        ['Specs', 'Dates', 'GlossTerm']]

    policy = [process_instance_id + ' and (MANUFACTURER or SUPPLIER)',
          process_instance_id + ' and (MANUFACTURER or (SUPPLIER and ELECTRONICS))',
          process_instance_id + ' and (MANUFACTURER or (SUPPLIER and SUPERVISOR))']

    g = open('your/data.json')

    message_to_send = g.read()

    input = {'process_id': process_instance_id,
        'entries': entries,
        'policy' : policy, 
        'message': message_to_send}

    response = requests.post('http://127.0.0.1:8888/dataOwner/cipher',
        json = input)
```