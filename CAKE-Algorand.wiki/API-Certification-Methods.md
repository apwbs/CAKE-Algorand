1. [POST /certification/](#post-certification)
2. [POST /certification/readpublickey/](#post-certificationreadpublickey)
3. [POST /certification/skmpublickey/](#post-certificationskmpublickey)
4. [POST /certification/attributecertification/](#post-certificationattributecertification)

## POST /certification/

This method is used to certify the actors involved in a given process. It requires a list of actors and their associated roles, which are sent in the request body in JSON format.

### Request Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| actors | list | Yes | A list of actors involved in the process |
| roles | dict | Yes | A dictionary containing the roles associated with each actor |

### Response Parameters

| Name | Type | Description |
|------|------|-------------|
| body | str | The ID of the certification process instance |
| status | int | The status code of the response (200 if successful) |

### Example Request

```python
import requests 

actors = ['ALICE', 'BOB']
roles = {'ALICE': ['MANUFACTURER', 'ELECTRONICS', 'SUPERVISOR'],
    'BOB': ['SUPPLIER', 'ELECTRONICS']}

input = {'actors': actors, 'roles': roles}

response = requests.post('http://127.0.0.1:8888/certification', json = input)
```

## Method: POST /certification/readpublickey/

This method is used to read the public keys of actors involved in a given process. It requires a list containing the actors' names, which is sent in the request body in JSON format.

### Request Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| actors | list | Yes | A list containing the names of actors |

### Response Parameters

| Name | Type | Description |
|------|------|-------------|
| status | int | The status code of the response (200 if successful) |

### Example Request

```python
import requests 

actors = ['ALICE', 'BOB']

input = {'actors': actors}

response = requests.post('http://127.0.0.1:8888/certification/readpublickey',
    json = input)

```


## Method: GET/POST /certification/skmpublickey/

This method is used to read the public key of the SKM (Secure Key Manager). It does not require any parameters.

### Response Parameters

| Name | Type | Description |
|------|------|-------------|
| status | int | The status code of the response (200 if successful) |

### Example Request

```python
import requests 

response = requests.post('http://127.0.0.1:8888/certification/skmpublickey')
```

## Method: POST /certification/attributecertification/

This method is used to certify the attributes of actors involved in a given process. It requires a dictionary containing the roles associated with each actor, which is sent in the request body in JSON format.

### Request Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| roles | dict | Yes | A dictionary containing the roles associated with each actor |

### Response Parameters

| Name | Type | Description |
|------|------|-------------|
| body | str | The ID of the certification process instance |
| status | int | The status code of the response (200 if successful) |

### Example Request

```python
import requests 

roles = {'ALICE': ['MANUFACTURER', 'ELECTRONICS', 'SUPERVISOR'],
    'BOB': ['SUPPLIER', 'ELECTRONICS']}

input = {'roles': roles}

response = requests.post('http://127.0.0.1:8888/certification/attributecertification',
    json = input)
```



