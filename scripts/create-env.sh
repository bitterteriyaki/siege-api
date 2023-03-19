# Copy the example environment file:
cp config/.env.example config/.env

# Create a Django secret key for the application:
SECRET_KEY=$(python3 -c 'from django.utils.crypto import get_random_string; print(get_random_string(64))')

# Set the secret keys in the environment file:
sed -i -r "s/^(DJANGO_SECRET_KEY=).*/\1$SECRET_KEY/" config/.env
sed -i -r "s/^(PUSHER_APP_ID=).*/\1$PUSHER_APP_ID/" config/.env
sed -i -r "s/^(PUSHER_KEY=).*/\1$PUSHER_KEY/" config/.env
sed -i -r "s/^(PUSHER_SECRET=).*/\1$PUSHER_SECRET/" config/.env
sed -i -r "s/^(PUSHER_CLUSTER=).*/\1$PUSHER_CLUSTER/" config/.env
