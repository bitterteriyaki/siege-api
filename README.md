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
git clone https://github.com/siegeapp/api.git

# entering the cloned repository folder
cd api

# installing the dependencies
poetry install

# performing database migrations
python manage.py migrate

# running the application
python manage.py runserver 0.0.0.0:8000
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
