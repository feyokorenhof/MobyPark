### INSTALL ###

docker compose -f docker-compose.yml up

## Current endpoints: ##

/auth/register:
email: str,
password: str,
name: str

/auth/login:
email: str,
password: str

/auth/users/{user_id}:
user_id: str

