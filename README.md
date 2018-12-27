# shortify
A URL shortening microservice built on top of Flask, Redis and Postgresql. Like existing URL shortening services, shortify associates a 8 character key to every long url. This key is employed to create a short "beautiful" URL of the form `<shortify_host>/go/<key>`, which redirects to the original URL. 

Under the hood, shortify utlises Redis to create a large map, mapping keys to URLs. PostgreSQL provides a persistant store from which the mapping table can be rebuilt after a failure. 


## Getting Started
### Prerequisites
  * Python 3 & Pip ( you probably should create a virtual environment )
  * Redis
  * PostgreSQL
  
### Installation
  1. __Local Installation__
  * Clone the repository
    ``` 
    git clone https://github.com/anubhavp28/shortify/ 
    cd shortify
    ```
  * Install python dependencies
    ```
    pip install -r requirements.txt
    ```
  * Open `config.sh` and provide your Redis & PostgreSQL config.
  * Shortify utilises env variables to get configuration details. Run the following command to set env variables.
    ```
    source config.sh
    ```
  * Run the development server.
    ```
    python shortify.py
    ```
  2. __Deployment with Docker__ (assuming that you have docker installed)
  * Clone the repository
    ```
    git clone https://github.com/anubhavp28/shortify/
    cd shortify
    ```
  * Build the image
    ```
    docker build ./ -t shortify
    ```
  * Run the image in a new container 
    ```
    docker run -p 8080:80 --env-file env.list shortify
    ```
  The service should be live at `localhost:8080`.
## License
This project is licensed under the MIT License - see the LICENSE.md file for details
