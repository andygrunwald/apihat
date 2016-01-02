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
$ docker pull andygrunwald/simple-webserver
$ docker run -d -p 5000:5000 andygrunwald/apihat
241cb569344f3b11126a842620167......
```

## Endpoints

### /identities

#### Retrieve identities

Method: GET

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
```

Possible response codes:

* 200 OK
* 404 Not Found

#### Add an identity

TODO

## TODO List

* TravisCI
* Native installation chapter
* Endpoint chapter
* License
* Contribution-Chapter
* Docker database