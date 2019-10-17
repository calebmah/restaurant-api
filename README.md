# Restaurant REST API Sample

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/fb4fbd8c5509ed1c5d66#?env%5BEnvironment%5D=W3sia2V5Ijoiand0IiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlfV0=)

## Table of Contents

* [About the Project](#about-the-project)
  * [Database Design](#database-design)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Start local webserver](#start-local-webserver)
  * [Create admin user](#create-admin-user)
  * [Access django admin](#access-django-admin)
  * [Running Tests](#running-tests)
* [REST API documentation](#rest-api-documentation)
  * [Get JSON Web Token](#get-json-web-token)
  * [Create Order](#create-order)
  * [Get All Orders](#get-all-orders)
  * [Get Orders from a Customer](#get-orders-from-a-customer)
  * [Get Orders from a Restaurant](#get-orders-from-a-restaurant)
  * [Get Specific Order](#get-specific-order)
  * [Get Cost for Orders from a Restaurant](#get-cost-for-orders-from-a-restaurant)
* [Future Improvements](#future-improvements)

## About The Project

This is a sample REST API for a restaurant ordering system. It supports various operations such as making an order and viewing placed orders. Aggregation functions such as finding the total cost of orders for a restaurant or the average quantity of items ordered are also available. Please refer to the [REST API documentation](#rest-api-documentation) for more detailed documentation.

This project was built using:

* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [djangorestframework-jwt](https://pypi.org/project/djangorestframework-jwt/)

### Database Design

For the purposes of this sample, the following database schema will be used.

![DatabaseSchema Picture](images/DatabaseSchema.png)

The User table represents the User model found in `django.contrib.auth`, while the Orders, Retaurants and MenuItems tables are defined in [`orders/models.py`](orders/models.py).

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Installation of the relevant packages can be done using [conda](https://docs.conda.io/projects/conda/en/latest/index.html). For instructions on installing conda on your operating system, please refer to the [documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation).

### Installation

1. Clone the repo
2. Create virtual environment using `environment.yml`

    ```sh
    conda env create -f environment.yml
    ```

3. Activate virtual environment

    ```sh
    conda activate django
    ```

4. Create a `.env` file that contains your secret key. This key is used by django to secure signed data. An example file [`.env.example`](.env.example) is provided for reference.

5. Run database migrations

    ```sh
    python manage.py migrate
    ```

## Usage

This section contains information on frequent actions required for this project.

### Create admin user

An admin user is required to login to the django admin site. A user is also required in order to use the REST APIs. To create one, run the following:

```sh
python manage.py createsuperuser
```

You will be prompted to enter your desired username, email and password. Fill in each field and press enter to continue.

```sh
Username: admin
Email address: admin@example.com
Password: **********
Password (again): *********
Superuser created successfully.
```

### Start local webserver

The default server runs on port 8000 on the IP address 127.0.0.1. For more information, refer to the [django documentation](https://docs.djangoproject.com/en/2.2/ref/django-admin/#runserver).

```sh
python manage.py runserver
```

Note that the server must be running before accessing the API endpoints or the django admin pages.

### Access django admin

The django admin page is located at `/admin/`, for example http://127.0.0.1:8000/admin/. Use the credentials of the user created in the [previous step](#create-admin-user) to log in. After logging in, you will be able to access the django admin page as seen below.

![DjangoAdmin Picture](images/DjangoAdmin.png)

The django admin page can be used to create, modify or delete users, restaurants, menu items or orders. To start, you probably want to create a restaurant and some menu items to assign to it.

### Running Tests

Automated tests for the REST APIs can be found in [`orders/tests.py`](orders/tests.py). They can be run using the following:

```sh
python manage.py test
```

## REST API documentation

This section documents all of the REST APIs currently available.

## **Get JSON Web Token**

----
  Authenticates using the supplied username and password, returning a valid JSON Web Token. A valid JSON Web Token is required to call the other REST APIs.

* **URL**

  /api/auth/token/

* **Method:**

  `POST`
  
* **Data Params**

   **Required:**

   `username=[string]` <br />
   `password=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
`{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:**
`{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}`

## **Create Order**

----
  Creates a new order from the supplied data params. Bearer Token required.

* **URL**

  /api/orders/

* **Method:**

  `POST`
  
* **Data Params**

   **Required:**

   `restaurant=[string]` <br />
   `quantity=[integer]` <br />
   `item=[string]`

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:**
`{
    "id": 1,
    "created": "2019-10-15T15:47:47.607267Z",
    "user": 1,
    "restaurant": "Burger",
    "quantity": 1,
    "item": "beef",
    "comments": "",
    "total_price": "2.00"
}`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:**
`{
    "restaurant": [
        "This field is required."
    ],
    "quantity": [
        "A valid integer is required."
    ],
    "item": [
        "Object with name=does_not_exist does not exist."
    ]
}`

  OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{
    "detail": "Authentication credentials were not provided."
}`

## **Get All Orders**

----
  Gets all orders from all restaurants, ordered by created date. Bearer Token required.

* **URL**

  /api/orders/

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
`[{
    "id": 1,
    "created": "2019-10-15T15:47:47.607267Z",
    "user": 1,
    "restaurant": "Burger",
    "quantity": 1,
    "item": "beef",
    "comments": "",
    "total_price": "2.00"
}]`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{
    "detail": "Authentication credentials were not provided."
}`

## **Get Orders from a Customer**

----
  Gets all the orders form a specific customer using the supplied customer id. Bearer Token required.

* **URL**

  /api/orders/customer/:customer_id/

* **Method:**

  `GET`
  
* **URL Params**

   **Required:**

   `customer_id=[integer]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
`[{
    "id": 1,
    "created": "2019-10-15T15:47:47.607267Z",
    "user": 1,
    "restaurant": "Burger",
    "quantity": 1,
    "item": "beef",
    "comments": "",
    "total_price": "2.00"
}]`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{
    "detail": "Authentication credentials were not provided."
}`

  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:**
`{
    "message": "Customer with id: 0 does not exist"
}`

## **Get Orders from a Restaurant**

----
  Gets all the orders form a specific restaurant using the supplied restaurant name. Bearer Token required.

* **URL**

  /api/orders/restaurant/:restaurant_name/

* **Method:**

  `GET`
  
* **URL Params**

   **Required:**

   `restaurant_name=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
`[{
    "id": 1,
    "created": "2019-10-15T15:47:47.607267Z",
    "user": 1,
    "restaurant": "Burger",
    "quantity": 1,
    "item": "beef",
    "comments": "",
    "total_price": "2.00"
}]`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{
    "detail": "Authentication credentials were not provided."
}`

  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:**
`{
    "message": "Restaurant with name: does_not_exist does not exist"
}`

## **Get Specific Order**

----
  Gets a specific order using the supplied order id. Bearer Token required.

* **URL**

  /api/orders/:order_id/

* **Method:**

  `GET`
  
* **URL Params**

   **Required:**

   `order_id=[integer]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
`{
    "id": 1,
    "created": "2019-10-15T15:47:47.607267Z",
    "user": 1,
    "restaurant": "Burger",
    "quantity": 1,
    "item": "beef",
    "comments": "",
    "total_price": "2.00"
}`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{
    "detail": "Authentication credentials were not provided."
}`

  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:**
`{
    "detail": "Not found."
}`

## **Get Cost for Orders from a Restaurant**

----
  Gets the total cost of all orders from a specific restaurant using the supplied restaurant id. Bearer Token required.

* **URL**

  /api/orders/cost/:restaurant_name

* **Method:**

  `GET`
  
* **URL Params**

   **Required:**

   `restaurant_name=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
`{
    "cost": 2.0
}`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{
    "detail": "Authentication credentials were not provided."
}`

  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:**
`{
    "message": "Restaurant with name: does_not_exist does not exist"
}`

## **Get Average quantity of items from a Restaurant**

----
  Gets the average quantity of items ordered by a specific customer from a specific restaurant using the supplied restaurant name and customer id. Bearer Token required.

* **URL**

  /api/orders/stats/average-quantity/:restaurant_name/:customer_id

* **Method:**

  `GET`
  
* **URL Params**

   **Required:**

   `restaurant_name=[string]` <br />
   `customer_id=[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
`{
    "average": 2.0
}`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{
    "detail": "Authentication credentials were not provided."
}`

  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:**
`{
    "message": "Restaurant with name: does_not_exist does not exist"
}`

  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:**
`{
    "message": "Customer with id: does_not_exist does not exist"
}`

## Future Improvements

This project serves as a sample, but could be improved in numerous ways. For instance:

1. REST APIs for modifying and deleting orders
2. Permissions to ensure users can only modify and delete orders that they created
3. REST APIs for creating, modifying and deleting restaurants and menu items
4. Extending an order to contain multiple types of items
