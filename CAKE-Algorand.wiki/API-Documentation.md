Welcome to the API Methods page of CAKE-Algorand!

The API documentation is divided into these sections:
- [**API Certification Methods**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/API-Certification-Methods): methods to interact with the API to read the keys and attribute certification to the actors involved in the process. These methods are used by the client to start a new process.
- [**API DataOwner Methods**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/API-DataOwner-Methods): methods to interact with the SDM server to cipher a new message.
- [**API Client Methods**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/API-Client-Methods): methods to interact with the SKM server to decrypt a message.

These pages contain a comprehensive list of all the methods available in the CAKE-Algorand API and their description. 

Although the python language is used in the examples it will also be possible to make requests to the server using other programming languages. The choice of this language is totally arbitrary.
In particular, the 'requests' library will be used. So all the python script will start with the following line:
```python
    import requests 

    #YOUR CODE
```