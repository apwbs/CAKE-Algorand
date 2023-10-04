- [Handshake](#handshake)
- [Generate Keys](#generate-keys)
- [Access Data](#access-data)

This section describes the methods that allow you to interact with the SKM Server, allowing you to make a handshake with the actors, generate a key and have access to encrypted messages.
### Handshake

Also in this case you need to perform the handshake, therefore it is necessary to indicate the address of the reader inside the dictionary given in input using the key 'reader address'. It is also necessary to enter the ID of the message to be decrypted using 'message_id' as key, and the process_id as in the previous step.

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

### Generate Keys

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

### Access Data

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

At this point it will be possible for the reader to make access requests for any slice_id of the message without having to carry out the previous two steps.