- [Handshake](#handshake)
- [Cipher](#cipher)

The guide in this section shows how to messages to the SDM in order to cipher them server using the API, allowing to cipher a message.
The following example is an instance of a message to be ciphered.

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

### Handshake
To make an handshake it is necessary to build a dictionary with the process instance id corresponding to the key 'process_id', and to send a post request to 'dataOwner/handshake'.
Note that the process instance id is the only value given as input from now on as an `int`.
```python
    import requests 

    process_instance_id = 1234567890 #Process id generated after the attribute certification
    
    input = {'process_id' : process_instance_id}

    response = requests.post('http://127.0.0.1:8888/dataOwner/handshake',
        json = input)
```

### Cipher
If the handshake operation is completed correctly, you can proceed with the encryption of the message.
You have to build a dictionary, with the described information associated with the following keys:
- `'process_id'` : the process_id showed at the end of attribute certification
- `'entries'` : a list in which each element is a group of entries of the message to be encrypted which will be associated with the same privacy. These groups are represented by a list of strings, where the strings are associated with the keys of the json file.
- `'policy'` : a list of strings containing a logical expression for each group of entries. In the logical expression it is possible to specify the associated process instance id and the roles of who has the right to read the associated entry.
The correct formatting can be seen in the next code example.
- `'message'` : a string generated from reading the json file containing the message to cipher

```python
    import requests 

    process_instance_id = 1234567890 #Process id generated after the attribute certification
    
    entries = [['ID', 'SortAs', 'GlossTerm'],
        ['Acronym', 'Abbrev'],
        ['Specs', 'Dates', 'GlossTerm']]

    policy = [str(process_instance_id) + ' and (MANUFACTURER or SUPPLIER)',
          str(process_instance_id) + ' and (MANUFACTURER or (SUPPLIER and ELECTRONICS))',
          str(process_instance_id) + ' and (MANUFACTURER or (SUPPLIER and MECHANICS))']

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