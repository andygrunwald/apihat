# apihat

A REST(ful) API for [MetricsGrimoire/sortinghat](https://github.com/MetricsGrimoire/sortinghat).

## Features

* Support for sortinghat methods:
	* `add`
	* `show`

## Installation

### Native

1. Install [MetricsGrimoire/sortinghat](https://github.com/MetricsGrimoire/sortinghat)
2. Install python dependencies: `pip install Flask flask-restful`
3. Start the app:
   ```
	$ ./app.py
	* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
	* ...
	```

### Docker

You can use the pre compiled docker image available from [Docker Hub](https://hub.docker.com/r/andygrunwald/apihat/).

TODO: Not complete here .. no config is available ... no database available

```sh
$ docker run -d -p 5000:5000 andygrunwald/apihat
241cb569344f3b11126a842620167......
```

## Configuration

Configuration of *apihat* is done by environment variables.
Checkout the table below for all supported variables.

| Name          | Default value | Description |
| ------------- |---------------| ------------|
| APIHAT_HOST   | 0.0.0.0       | IP that this API is listen to |
| APIHAT_PORT   | 5000          | Port that this API is listen to |
| APIHAT_DEBUG  | False         | Debug mode of apihat |

To configure [sortinghat](https://github.com/MetricsGrimoire/sortinghat) (the software this api is based on) we only support their environment variables as well.
Checkout the [README](https://github.com/MetricsGrimoire/sortinghat/blob/master/README.md) of sortinghat to get details about this.

## Endpoints

### /init

* Method: POST
* sortinghat command: `init`
* Arguments:
	* `name` (required): Name of the init database
* Possible response codes:
	* 201 Created: Everything went well
	* 400 Bad Request: Name was not supplied
	* 500 Internal Server Error: Something went wrong

Example:

```bash
$ curl -X POST \
		-H "Content-Type: application/json" \
		-d '{"name":"registry"}' \
		http://apihat:5000/init
{
    "name": "registry"
}
```

### /identities

#### Retrieve identities

* Method: GET
* sortinghat command: `show`
* Arguments:
	* `term` (optional): Term to filter the response identites
* Possible response codes:
	* 200 OK: Everything went well
	* 404 Not Found: Term not found in database

Example:

```bash
$ curl -X GET http://apihat:5000/identities
{
    "identities": [
        {
            "identities": [
                {
                    "email": "max@example.com",
                    "id": "0067ffa82acc2721670f13e26bf2548a98458579",
                    "name": "Max Muster",
                    "source": "gerrit",
                    "username": "",
                    "uuid": "0067ffa82acc2721670f13e26bf2548a98458579"
                }
            ],
            "profile": null,
            "uuid": "0067ffa82acc2721670f13e26bf2548a98458579"
        },
        {
            "identities": [
                {
                    ...
                }
            ],
            "profile": null,
            "uuid": "01b98cd2fdd2a2802e3168c5b54bfc50ff384fe5"
        },
        ...
    ]
}
```

#### Add an identity

* Method: POST
* sortinghat command: `add`
* Possible response codes:
	* 201 Created: Everything went well and the identity was created
	* 400 Bad Request: Matcher not supported / Source is empty / All parameters are empty
	* 404 Not Found: UUID not found in registry
	* 409 Conflict: Identity already exists

Example:

```bash
$ curl -X POST -d 'username=maxwell&email=max@example.com&source=scm' http://apihat:5000/identities
{
    "id": "7fcf59c00ee2ece02824adb48d65edcaae755e17",
    "uuid": "7fcf59c00ee2ece02824adb48d65edcaae755e17"
}
```

### /identities/<uuid>

#### Retrieve a specific identity

* Method: GET
* sortinghat command: `show`
* Possible response codes:
	* 200 OK: Everything went well
	* 404 Not Found: If the identity can`t be found

Example:

```bash
$ curl http://apihat:5000/identities/7fcf59c00ee2ece02824adb48d65edcaae755e17
{
    "identities": [
        {
            "email": "max@example.com",
            "id": "7fcf59c00ee2ece02824adb48d65edcaae755e17",
            "name": null,
            "source": "scm",
            "username": "maxwell",
            "uuid": "7fcf59c00ee2ece02824adb48d65edcaae755e17"
        }
    ],
    "profile": null,
    "uuid": "7fcf59c00ee2ece02824adb48d65edcaae755e17"
}
```

### /ping

Small ping / health endpoint to check if the service is up.

* Method: GET
* sortinghat command: `show`
* Possible response codes:
	* 200 OK: Everything went well

Example:

```bash
$ curl http://apihat:5000/ping
pong
```

## TODO List

* TravisCI
* Native installation chapter
* License
* Contribution-Chapter
* Docker database
* http://stackoverflow.com/questions/14112336/flask-request-and-application-json-content-type