# Makefile for Swamp Courier Docker image
# This Makefile automates the process of building and running the Swamp Courier Docker image.
# Useful for local development.

# Build the Docker image
build:
	docker build -t swamp-courier .

# Run the container
run:
	docker run --rm -it --env-file .env swamp-courier

# Stop and remove all containers
clean:
	docker container prune -f

# default action
do:
	docker build -t swamp-courier .
	docker run --rm -it --env-file .env swamp-courier
