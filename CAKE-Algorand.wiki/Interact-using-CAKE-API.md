CAKE also has an API to manage its interaction, this section describes its structure and use.

In the following sub-pages it is described step by step how to use the API to interact correctly with the system. 

Although the python language is used in the examples it will also be possible to make requests to the server using other programming languages. The choice of this language is totally arbitrary.
In particular, the 'requests' library will be used. So all the python script will start with the following line:
```python
    import requests 

    #YOUR CODE
```


The API step-by-step guide is divided into these sections:
- [**Create a new process**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Create-a-new-process): how to read the keys of the actors involved in the process and assign the desired roles to them, and creating a new process.
- [**Cipher message**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Cipher-message): how to interact with the SDM server to cipher a new message.
- [**Decrypt message**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Decrypt-message): how to interact with the SKM server to decrypt a message.
