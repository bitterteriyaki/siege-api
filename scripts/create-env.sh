# copy the example environment file:
cp config/.env.example config/.env

# create a secret key for the application:
SECRET_KEY=$(python3 -c 'from django.utils.crypto import get_random_string; print(get_random_string(64))')

# set the secret key in the environment file:
sed -i "s/__EDIT_ME__/$SECRET_KEY/" config/.env
