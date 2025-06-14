# Docker

runs software/scripts in containers. (isolated)

example:
- Cont 1: Ubuntu Data pipeline (python, pandas, postgres, etc)
- Cont 2: Postgres DB
- Cont 3: pgAdmin

Uses:
- Reproducibility
- testing enviroment, local experiments
- Integration tests (CI/CD)
- Running pipelines in the cloud (AWS batch, Kubernetes jobs, etc)

## Docker image

Snapshot of the container with instructons and configurations.

Used to run this in another enviroment (GCP kubernetes, AWS batch, etc)


## Docker file

We specify how to create the image. Instructions to follow to create a new image

Example docker file
  
    FROM python:3.9

    #What to run inside the image when loading
    RUN apt-get install wget
    RUN pip install pandas sqlalchemy psycopg2 pyarrow

    #Location in the image to copy the file
    WORKDIR /app
    #Copies the file in this directory to the workdir inside the container
    COPY ingest_data.py ingest_data.py

    #Tells the container what to run once the image is loaded
    ENTRYPOINT [ "python", "ingest_data.py"]

## Docker commands

`docker run -it (image name) bash`
  
  Runs the image in interactive mode (-it).
  
  it tells docker that we want to do other commands and interact with the terminal
    
  bash tells them we want to run bash inside the container

  `docker run -it --entrypoint=bash (image)`

  Uses bash as an entrypoint, regardless what the ENTRYPOINT/CMD is in the image

  `docker build -t (image name):(version) .`

  Creates the image from the Dockerfile. Dot tells it to create image in this directory.


## Container commands

`exit` Exits the container

## Python

      import sys
      file = sys.argv[0] # File name
      arg1 = sys.argv[1] # first argument passed

## General terminal commands
- ls: List of directories and files
- pwd: Outputs the present working dir
