# apihat

A REST(ful) API for [MetricsGrimoire/sortinghat](https://github.com/MetricsGrimoire/sortinghat).

## Features

* Support for sortinghat methods:
	* `add`
	* `init`
	* `show`

## Installation

### Native

1. Install [MetricsGrimoire/sortinghat](https://github.com/MetricsGrimoire/sortinghat)
2. Install python dependencies: `pip install Flask flask-restful`
3. Start the app:

   ```
	$ ./apihat/app.py
 	* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
	* ...
	```

### Docker

You can use the pre compiled docker image available from [Docker Hub](https://hub.docker.com/r/andygrunwald/apihat/).

At first we need a database. Lets use MySQL:

```sh
$ docker run --name mysql \
             -e MYSQL_USER=sortinghat \
             -e MYSQL_PASSWORD=sortinghat \
             -e MYSQL_ROOT_PASSWORD=sortinghat \
             -d mysql
```

Now we start apihat with the sortinghat and apihat configuration and use the database we started a minute ago:

```sh
$ docker run -p 5000:5000 \
             -e SORTINGHAT_DB_HOST=mysql \
             -e SORTINGHAT_DB_USER=root \
             -e SORTINGHAT_DB_PASSWORD= \
             -e SORTINGHAT_DB_DATABASE=sortinghat \
             -d andygrunwald/apihat
```

Afterwards we do a small test if the api is running (change the host `apihat` to your docker host IP):

```bash
$ curl http://apihat:5000/ping
{"content": "pong"}
```

Congratulations! Everything up and running!
You can now continue with [initializing a registry](#init) and [adding identities](#add-an-identity). Have fun!

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
* HTTP Body attributes:
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
* Query parameters:
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
* HTTP Body attributes:
	* `name` (optional): Name of the identity
	* `email` (optional): Email of the identity
	* `username` (optional): Username of the identity
	* `uuid` (optional): UUID to assign the identity
	* `source` (optional): Source of the identity
	* `matching` (optional): Matching mechanism (email (default), email-name, see sortinghat for more)
* Possible response codes:
	* 201 Created: Everything went well and the identity was created
	* 400 Bad Request: Matcher not supported / Source is empty / All parameters are empty
	* 404 Not Found: UUID not found in registry
	* 409 Conflict: Identity already exists

Example:

```bash
$ curl -X POST \
		-H "Content-Type: application/json" \
		-d '{"username":"maxwell","email":"max@example.com","source":"scm"}' \
		http://apihat:5000/identities
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

## Contribution

Contribution is highly welcome.
It doesn`t matter if you are able to modify source code, create a Pull Request, commenting issues or talk about *apihat* at the next usergroup meetup.
Every kind of contribution is welcome here.

If you are unsure about something [open a new issue](https://github.com/andygrunwald/apihat/issues/new) and ask your question there.
The team will be happy to help.

## TODO List

* TravisCI
* License