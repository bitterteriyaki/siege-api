## 0.5.0 (01/03/2023)

- `ci`: add a workflow to upload the application do GitHub Packages

## 0.4.0 (26/02/2023)

### Features

- `apps/messages`: initial messages app
- `apps/members`: add typings to members serializer
- `apps/channels`: rewrite channels app
- `apps/members`: rewrite members app
- `apps/authentication`: rewrite authentication app
- `apps/guilds`: rewrite guilds app
- `apps/users`: rewrite users app
- `core/exceptions`: change error response payload schema
- `apps`: add typings to tests
- `apps`: add typings to the application
- `app/channels`: initial channels system

### Fixes

- `apps/users`: add a table name for users model
- `apps/messages`: raise an error when the user tries to send a message to itself
- `apps/messages`: change messages model table name
- `apps/messages`: fix message error when the user does not exist

### Refactors

- `apps/messages`: use `get_user` helper function

## 0.3.0 (01/02/2023)

### Features

- `apps/members`: add endpoint to retrieve all the members of a guild
- `apps/members`: move guild members serializer to `members` app
- `apps/members`: implement guild members to its own app
- `apps/guilds`: add guild members implementation
- `apps/guilds`: add initial guilds system
- `apps/users`: implement `/users/<user_id>` route
- `apps/auth`: add an authentication workflow
- `apps/users`: remove `/auth` route from application
- `apps/users`: remove useless checks from `User` object manager
- `apps/users`: change fields from `User` model
- `server`: create separated environments for development and CI
- `apps/auth`: add initial authentication app

### Fixes

- `core/exceptions`: remove case when the response is null
- `apps/users`: remove string representation of the user
- `server/settings`: CI environment must inherit development environment
- `apps/users`: use user's IDs instead of a dummy ID
- `apps/auth`: raise `PermissionDenied` when the user does not exist or is not active instead of `ValidationError`
- `apps/users`: remove `created_at` from `User` schema

### Refactors

- `members/views`: use viewsets to retrieve all members
- `guilds`: add `get_guild` helper function

## 0.2.0 (06/01/2023)

### Features

- `core`: improve error response JSON schema
- `apps/users`: implement Snowflake IDs to users
- `apps/users`: move token generation logic to `apps/users` folder and implement token versioning
- `apps/users`: create initial tokens service
- `apps/users`: create initial users app

### Fixes

- `apps/users`: fix renderer context response data
- `apps/users`: change validation error response schema
- `apps/users`: fix exception handler response data
- `apps/users`: raise error if not tags were available
- `server/settings`: fix database configuration

### Refactors

- `apps/users`: change logic layer to its own module
- `apps/users`: move `core` and `apps` folders to the root folder

## 0.1.0 (02/01/2023)

### Features

- `server`: add initial server development
