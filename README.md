

# Best Price Finder

This DRF application can be used to determine the cheapest/best combination of offers/pricing blocks, based on provided start date, number of nights and the product ID.

## Use case

    Available pricing blocks:
    
    A [2018. 01. 01. - 2018. 01. 10.] 2 nights for 100 EUR
    B [2018. 01. 02. - 2018. 01. 10.] 2 nights for 120 EUR
    C [2018. 01. 03. - 2018. 01. 10.] 2 nights for 123 EUR
    D [2018. 01. 03. - 2018. 01. 10.] 1 night for 60 EUR
    
    Start date: 2018. 01. 01.
    Number of nights: 5
    Best offer combo: A (2 nights, 100 EUR), A (2 nights, 100 EUR), D (1 night, 60 EUR) = 260 EUR

## GET request example
curl -v "http://127.0.0.1:8000/best_price/?start_date=2020-01-08&num_nights=1&product_id=1"  | jq .

    {
      "price": "100.00",
      "currency": "£",
      "blocks": [
        {
          "id": 2,
          "start_date": "2020-01-08",
          "end_date": "2020-01-15",
          "nights": 1,
          "price": "100.00",
          "product_id": 1
        }
      ]
    }

# How to run

The project was built by using:

 1. Python 3.6
 2. Django 1.11
 3. Django Rest Framework 3.7.7
 4. ReactJS (ES6) using Webpack and Babel 

To run it, please ensure that you have Python 3.6 and node package manager installed on your platform. 

The following steps apply for the OSX environment. We're using Python3 venv module to create a lightweight virtual environment.

## Initial steps

    1. git clone https://github.com/jklarica/best_price_finder.git
    2. cd best_price_finder
    3. brew install python3
    4. python3 -m ensurepip --upgrade
    5. python3.6 -m venv python3.6_env
    6. source python3.6_env/bin/activate
    7. pip install -r requirements.txt

## REST API

    1. cd best_price_finder
    2. python manage.py makemigrations products
    3. python manage.py migrate
    4. python manage.py loaddata products/fixtures/initial_data.yaml
    5. python manage.py test
    6. python manage.py runserver

Server should now be accessible at [http://localhost:8000/](http://localhost:8000/). 

Example requests:

    1. http://127.0.0.1:8000/best_price/?format=api&num_nights=15&product_id=1&start_date=2020-01-1
    2. http://127.0.0.1:8000/product/
    3. http://127.0.0.1:8000/pricing_block/
    
## Frontend

This should be executed in another shell instance; navigate to the project root directory and then:

    1. cd frontend
    2. npm install
    4. npm run dev

Finally, navigate to [http://localhost:8080/](http://localhost:8080/) to access the frontend.