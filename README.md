
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

To run it, please ensure that you have Python 3.6 installed on your platform. 

The following steps apply for the OSX environment. We're using Python3 venv module to create a lightweight virtual environment.

    1. git clone https://github.com/jklarica/best_price_finder.git && cd best_price_finder
    2. brew install python3
    3. python3 -m ensurepip --upgrade
    4. python3.6 -m venv python3.6_env
    5. source python3.6_env/bin/activate
    6. pip install -r requirements.txt
    7. cd best_price_finder
    8. python manage.py makemigrations products
    9. python manage.py migrate
    10. python manage.py loaddata products/fixtures/initial_data.yaml
    11. python manage.py test
    12. python manage.py runserver
    
Finally, you can use the cURL command above to test the endpoint.