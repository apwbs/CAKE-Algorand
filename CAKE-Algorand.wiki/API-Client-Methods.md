1. [POST /client/handshake](#post-clienthandshake)
2. [POST /client/generateKey](#post-clientgeneratekey)
3. [POST /client/accessData](#post-clientaccessdata)

## POST /client/handshake

Make an handshake between the client and the SKM Server. It requires the process instance id as parameter, with the message_id and the reader address.

### Request Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| process_id | int | Yes | The ID of the process instance |
| message_id | str | Yes | The ID of the message to be read |
| reader_address | str | Yes | The address of the reader |

### Response Parameters
| Name | Type | Description |
|------|------|-------------|
| status | int | The status code of the response (200 if successful) |

### Example Request

```python
import requests

process_instance_id = 314159265 #Process id generated after the attribute certification
message_id = '13846106420650213324' 
reader_address = 'N2C374IRX7HEX2YEQWJBTRSVRHRUV4ZSF76S54WV4COTHRUNYRCI47R3WU'

input = {'process_id' : process_instance_id,
    'message_id': message_id,
    'reader_address' : reader_address}

response = requests.post('http://127.0.0.1:8888/client/handshake',
    json = input)
```

##    

Generating the key to decrypt the message requires the process instance id, the message id and the reader address.
It also requires that the reader has done a handshake with the SKM server in the past for the requested process and message.

### Request Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| process_id | int | Yes | The ID of the process instance |
| message_id | str | Yes | The ID of the message to be read |
| reader_address | str | Yes | The address of the reader |

### Response Parameters
| Name | Type | Description |
|------|------|-------------|
| status | int | The status code of the response (200 if successful) |

### Example Request

```python

import requests

process_instance_id = 314159265 #Process id generated after the attribute certification
message_id = '13846106420650213324'
reader_address = 'N2C374IRX7HEX2YEQWJBTRSVRHRUV4ZSF76S54WV4COTHRUNYRCI47R3WU'

input = {'process_id' : process_instance_id,
    'message_id': message_id,
    'reader_address' : reader_address}

response = requests.post('http://127.0.0.1:8888/client/generateKey',
    json = input)
```

## POST /client/accessData

Accessing a portion of information of a message requires the process instance id , the message id, the slice_id and the reader address. It also requires that the reader has done a handshake and key generation with the SKM server in the past for the requested process and message.

### Request Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| process_id | int | Yes | The ID of the process instance |
| message_id | str | Yes | The ID of the message to be read |
| slice_id | int | Yes | The ID of the slice to be read |
| reader_address | str | Yes | The address of the reader |

### Response Parameters
| Name | Type | Description |
|------|------|-------------|
| status | int | The status code of the response (200 if successful) |

### Example Request

```python
import requests 

process_instance_id = 314159265 #Process id generated after the attribute certification
slice_id = '13846106420650213324'
message_id = '14845106402133206524'
reader_address = 'N2C374IRX7HEX2YEQWJBTRSVRHRUV4ZSF76S54WV4COTHRUNYRCI47R3WU'

input = {'process_id' : process_instance_id,
    'slice_id' : slice_id,
    'message_id': message_id,
    'reader_address' : reader_address}

response = requests.post('http://127.0.0.1:8888/client/accessData',
    json = input)
```
