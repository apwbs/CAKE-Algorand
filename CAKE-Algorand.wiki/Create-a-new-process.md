- [Read keys and attribute certification](#read-keys-and-attribute-certification)
- [Read public key](#read-public-key)
- [Read SKM's key](#read-skms-key)
- [Attribute certification](#attribute-certification)

### Read keys and attribute certification

Using the API it is possible to read the keys of the skm server actors, and assign the desired roles to the actors involved.
It is necessary to define a list with the names of the actors, remember that the name must be the same used inside the env when the address and public key of the actor are specified.
In addition to a list of strings with the actors involved, a dictionary must be defined and it associates the roles assigned to the actors involved. Each actor can have multiple roles, and each role can be assigned multiple times.
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

The response of the request made to the server consists of the generated process instance id.
Using the library in the example it can be accessed with the following line of code:
```python
    response.text
```

This request can be divided in the following three different requests to the api server, like in the following three subsections. For a correct functioning it is necessary to carry out these operations in the proposed order.

### Read public key

Using the method in the example it is possible to ask to server to read the keys of the actors stored in the '.env' files.
It is necessary to construct a list with the names of the actors, and then a insert the list into a dictionary with the key 'actors', as described above. This dictionary is used as input like in the example.
```python
    import requests 

    actors = ['MANUFACTURER', 'SUPPLIER1', 'SUPPLIER2']

    input = {'actors': actors}

    response = requests.post('http://127.0.0.1:8888/certification/readpublickey',
        json = input)

```

### Read SKM's key

Using the method in the example is possible to ask to the server to read the key of the SKM server stored in the '.env'.
This method does not need any input.

```python
    import requests 

    response = requests.post('http://127.0.0.1:8888/certification/skmpublickey')

```

### Attribute certification

This method allows you to certify on the blockchain the roles assigned to the actors, whose key has previously been read. A dictionary must be defined and it associates the roles assigned to the actors involved. Each actor can have multiple roles, and each role can be assigned multiple times.
This dictionary will have to be inserted in a dictionary, with 'roles' as key, and given as input as in the following example during the request to the api server.

```python
    import requests 

    roles = {'MANUFACTURER': ['MANUFACTURER'],
        'SUPPLIER1': ['SUPPLIER', 'ELECTRONICS'],
         'SUPPLIER2': ['SUPPLIER', 'MECHANICS']}

    input = {'roles': roles}

    response = requests.post('http://127.0.0.1:8888/certification/attributecertification',
        json = input)

```

The response of the request made to the server consists of the generated process instance id.
Using the library in the example it can be accessed with the following line of code:
```python
    response.text
```