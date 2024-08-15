#!/bin/bash

# Generate a new Django secret key
generate_django_secret_key() {
    python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
}

# Call the function and store the result
SECRET_KEY=$(generate_django_secret_key)

# Print the generated secret key
echo "Generated Django Secret Key:"
echo "$SECRET_KEY"

# Optionally, you can append the secret key to a .env file
echo "SECRET_KEY='$SECRET_KEY'" >> .env