#!/bin/bash

# Wait for the app service to be fully operational
until [ $(curl -s -o /dev/null -w "%{http_code}" http://app:8000/) -eq 200 ] || [ $(curl -s -o /dev/null -w "%{http_code}" http://app:8000/) -eq 302 ]; do
  echo "Waiting for app to be fully operational..."
  sleep 3
done

# Start Celery Worker
exec "$@"
