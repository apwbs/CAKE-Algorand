This repository contains the **Algorand**-based version of the CAKE approach presented in the paper "[Fine-grained Data Access Control for
Collaborative Process Execution on Blockchain](https://arxiv.org/abs/2207.08484)" (DOI: [10.1007/978-3-031-16168-1_4](https://doi.org/10.1007/978-3-031-16168-1_4); slides are available on [SlideShare](https://www.slideshare.net/EdoardoMarangone/finegrained-data-access-control-for-collaborative-process-execution-on-blockchain-253133788)). Please find and fork the latest release based on **Ethereum** at [github.com/apwbs/CAKE-Ethereum](https://github.com/apwbs/CAKE-Ethereum/)!

In this [Docker Hub repository](https://hub.docker.com/repository/docker/apwbs/cake/general) there are the two Docker Images 
for the Ethereum and Algorand implementation of the CAKE approach.

This GitHub Wiki contains the following pages:
* [**Home**](https://github.com/MichaelPlug/CAKE-Algorand/wiki): This page.
* [**Requirements**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Requirements): A description of the requirements to run CAKE, from the docker execution to the .env file configuration.
* [**Run CAKE locally**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Run-CAKE-locally): A step-by-step guide to run CAKE locally.
* [**Run CAKE API**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Run-CAKE-API): A step-by-step guide to run CAKE API locally.
* [**Interact using API**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Interact-using-CAKE-API): A step-by-step guide to interact with CAKE API.
   * [**Create a new process**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Create-a-new-process): How to create a new process using CAKE-API
   * [**Cipher message**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Cipher-message): How to cipher a message using CAKE-API
   * [**Decrypt messages**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/Decrypt-message): How to decrypt a message using CAKE-API
* [**API Documentation**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/API-Documentation): An overview of the API methods available in CAKE-API
   * [**API Certification Methods**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/API-Certification-Methods): Documentation of the API methods to read the keys and attribute certification to the actors involved in the process
   * [**API DataOwner Methods**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/API-DataOwner-Methods): Documentation of the API methods to cipher a new message
   * [**API Client Methods**](https://github.com/MichaelPlug/CAKE-Algorand/wiki/API-Client-Methods): Documentation of the API methods to decrypt a message