# apihat

A REST(ful) API for [MetricsGrimoire/sortinghat](https://github.com/MetricsGrimoire/sortinghat).

## Features

* Support for sortinghat methods:
	* `add`
	* `show`

## Installation

### Native

TODO

### Docker

The docker image is available at [Docker Hub](https://hub.docker.com/r/andygrunwald/apihat/).

```sh
$ docker run -d -p 5000:5000 andygrunwald/apihat
241cb569344f3b11126a842620167......
```

TODO: Not complete here .. no config is available ...

## Endpoints

### /identities

#### Retrieve identities

* Method: GET
* sortinghat command: `show`
* Possible response codes:
	* 200 OK: Everything went well

Example call:

```bash
$ curl http://apihat:5000/identities
```

Example response:

```javascript
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

Example call:

```bash
$ curl -X POST -d 'username=maxwell&email=max@example.com&source=scm' http://apihat:5000/identities
```

Example response:

```javascript
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

Example call:

```bash
$ curl http://apihat:5000/identities/7fcf59c00ee2ece02824adb48d65edcaae755e17
```

Example response:

```javascript
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