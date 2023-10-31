#!/bin/bash

# Create network
docker network create simbirgo_simbirgo-network

# Up db
docker compose up database -d

# Build app image
docker build -t simbirgo-monolit --target slim .

# Run migration
docker run --network simbirgo_simbirgo-network simbirgo-monolit monolit database migrations migrate

# Start app
docker run --network simbirgo_simbirgo-network -p "8000:8000" simbirgo-monolit monolit run
