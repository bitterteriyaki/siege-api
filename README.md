# Siege API

Repository for Siege API Service.

## Prerequisites

Project requirements are always specified in the [`.tool-versions`](https://github.com/siegeapp/api/blob/main/.tool-versions) file:

* Python 3.11.1
* PostgreSQL 15.1
* Poetry 1.3.2

See the [Poetry installation guide](https://python-poetry.org/docs/#installation).

## Build

```sh
# cloning the repository
$ git clone https://github.com/siegeapp/api.git

# entering the cloned repository folder
$ cd api

# installing the dependencies
$ poetry install

# creating the `.env` file
$ ./scripts/create-env.sh

# performing database migrations
$ python manage.py migrate

# running the application
$ python manage.py runserver 0.0.0.0:8000
```

If you prefer, there is also a Docker (and Docker Compose) image in the repository:
```sh
# build the image and start the application
docker compose build
docker compose up
```
If everything has run correctly, you will be able to access the API via the URL `http://localhost:8000`.

## Conventions & Code Quality

### Git Hooks

This project has [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) (through the [`pre-commit`](https://pre-commit.com) library) that help with development and ensure code quality. It is highly recommended that you use these hooks!

```sh
# install all needed hook types
$ pre-commit install \
  --hook-type commit-msg \
  --hook-type pre-push \
  --hook-type pre-commit

# it's done! now you can program normally, and when
# you go to commit something, the hooks will run.
```

## Authors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/bitterteriyaki">
        <img src="https://avatars.githubusercontent.com/u/82721542" width="100px;" />
        <br>
        <sub>
          <b>@bitterteriyaki</b>
        </sub>
      </a>
      <br>
      <sub>
        Maintainer
      </br>
    </td>
  </tr>
</table>
