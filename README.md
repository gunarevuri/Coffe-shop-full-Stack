# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

Developed backend, which if flask based application and Implementing token-based authentication and authorization for each request from the client using a third-party tool Auth0. For each REST API request from the client, the token is verified and check whether the client can make a request to that endpoint by Implementing role-based control design patterns in API. The token is then verified in backend by creating rsa-key and decrypting token and checking whether payload contains permissions.


Make sure you had enabled vertual environment.If you are using mac then follow below commands

```
cd project_directory

python3 -m venv env

source env/bin/activate


```

Then clone the project 

```
git clone https://github.com/gunarevuri/Coffe-shop-full-Stack.git
```

Run backend server before running frontend as frontend needs some data from backend to display the web page.


To run this app locally you should create your own Auth0 account.

```
https://auth0.com/
```

In order to run this application follow below steps:


- create a tenant domain and then select web based application while creating applicaiton, 

- Then create specific API, name of audience

    - Then it will automatically generate client id
    
- Then go to ./backend/api.py file replace my Auth0 tenant domain with your Auth0 domain and API audience too. 

- If you want to change algorithm used to encrypt header token make sure it is changed in Auth0 account and same algorithm is used to decrypt token.In my implementation I used RS256 to sign token and decrypt token to get payload.and check for permissions


In my Auth0 account used to 3 types of roles public, barista and manager. 

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.



## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

README.md file present in backend directory will have the all documentation like how to run backend.
[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
# Coffe-shop-full-Stack
