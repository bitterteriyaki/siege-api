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
