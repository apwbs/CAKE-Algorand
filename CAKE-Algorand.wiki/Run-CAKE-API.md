CAKE also has an API to manage its interaction, this section describes its structure and use.

- [Requirement](#requirement)
- [Initialization](#initialization)
- [Run API](#run-api)
- [Run SDM and SKM servers](#run-sdm-and-skm-servers)

### Requirement
You need to install flask to run the API server on your machine. 
Open the terminal and run `pip install flask`.

### Initialization
The database resetting and the deployment of the contract cannot be done using the API, you have to open your terminal and run in 'CAKE-Algorand/architecture' `sh resetDB.sh` and `sh deploy.sh`.

### Run API
At this point is possible to lunch the API, running `python3 API/api.py`.

The terminal will show the base path to use to interact the API (in the following example it is 'http://localhost:8888/')

```
root@7e473ad21d74:/CAKE-Algorand/architecture# python3 API/api.py 
 * Serving Flask app 'api' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://localhost:8888/ (Press CTRL+C to quit)
```

At this point the API is running, an it is possible interact with it.
To test if the API is correctly working you can run this script and check if the request status is 200.

```python
    import requests

    response = requests.get('http://localhost:8888/')
```

### Run SDM and SKM servers

After the client generates a process_id, you need to put it in the .env file, after which you can launch the SDM and SKM servers, running on your terminal `python3 sdm_server.py` and `python3 skm_server.py`.
Then, copy the SDM and SKM server addresses in the .env file, and the API is ready to be used for ciphering and deciphering messages.

```python
SERVER = "172.17.0.2"
PROCESS_INSTANCE_ID=2494707248652133556
```
