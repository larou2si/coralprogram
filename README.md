# Coral Technical Test

## make sure that docker is well installed on your local machine and is already running
```
docker --version
```
## To create our Django project and build our docker image, we need to create a docker-compose.yml file where we have define the images that we will work with. for example in this project, we use a container of postgresql database into our django application:

### build our image then run it to become a container
```
# clone the project from github repo
    cd coralprogram
    docker-compose up --build
# Now open the browser and go to http://localhost:8000 to verify the application is running well

```


## Task1
```
# to generate data for an empty or even existing DB, we used the package 'faker' to generate our random data
    %docker-compose run --rm multiversetask python manage.py generate_faker_data

-> a json will created 'sample.json' = a dump of our database in json format

# to ensure that we work with same DATA use the dumped file 'sample.json'
    %docker-compose run --rm multiversetask python manage.py loaddata sample.json
```

## Task2 , Task3
#### this project provide for our users a list of endpoints to fetch and aggregate our DB
```
apparts/ : GET API
    fetch all appartements

actifappartement/ : GET API
    retrieve the appartement which its program is actif

rangeprice/ : GET API, accepts as query params: min_price and max_price | both are float
    get appartements which their price in a specific range passed in the request

programshaspiscine/ : GET API
    get list of Program which at least one of his appartements had 'piscine'

promo/ : GET API, accepts as query params: code | string
    recieve a discount by 5% when you have the right code :)

recommandation/<str:date>/ : GET API
    this endpoint should accept date with this format month-day-year
```

## Perspective:
```
- we should refine the workflow used in the Task1
- secret our API with authentification, Tokens..
- develop an analytic dashboard where we could plot the correlation between 'surface and prix'
```


## author: coral-io