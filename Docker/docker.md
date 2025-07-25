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
  
  In the example it does not run the pipeline.py file.

  `docker build -t (image name):(version) .`

  Creates the image from the Dockerfile. Dot tells it to create image in this directory.

  `docker image prune -a` removes inactive images

  `docker images`
  checks created images. -a includes dangling images
  
  `docker ps` 
  checks running containers. -a includes all (running, stopped, exited)

  `docker network create pg-network` creates a network in docker

  `docker stop [container id]` stopes container

      docker run -it \
      -e POSTGRES_USER="root" \
      -e POSTGRES_PASSWORD="root" \
      -e POSTGRES_DB="ny_taxi" \
      -v c:/Users/nphil/Learning/DEzoomcamp/Practice module 1/ny_taxi_postgres_data:/var/lib/postgresql/data \
      -p 5432:5432 \
      --network= mynet \
      postgres:13

docker runs image with those env variables (-e)
.links folder in the system with containers data directory (-v)

network lets pg connect with postgres

example -v
C:\Users\nphil\Learning\DEzoomcamp\Practice module 1
-v c:/Users/alexe/git/data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \

### One off run commands in CLI
In linux WSL:

    docker run -it \
      -e POSTGRES_USER="root" \
      -e POSTGRES_PASSWORD="root" \
      -e POSTGRES_DB="ny_taxi" \
      -v "$PWD/ny_taxi_postgres_data:/var/lib/postgresql/data" \
      -p 5432:5432 \
      --network=pg-network \
      --name pg-database \
      postgres:13

pgadmin container - to create the container in a single run.

    docker run -it \
      -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
      -e PGADMIN_DEFAULT_PASSWORD="root" \
      -p 8080:80 \
      --network=pg-network \
      --name pgadmin \
      dpage/pgadmin4


port admin:container

## pgadmin

create server:
- Name: any
- host address: pg-database  - Host of the pg database (container name with pg database. can be localhost)
- port: 5432   - Port where postgres is mapped


## Dockercompose 

    services:
      pgdatabase:
        image: postgres:13
        # Enviroment variables
        environment: 
          - POSTGRES_USER=root
          - POSTGRES_PASSWORD=root
          - POSTGRES_DB=ny_taxi
        volumes:
          - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
        ports:
          - "5432:5432"
      pgadmin:
        image: dpage/pgadmin4
        environment:
          - PGADMIN_DEFAULT_EMAIL=admin@admin.com
          - PGADMIN_DEFAULT_PASSWORD=root
        ports:
          - "8080:80"

need to specify a port for postgres to communicate to the db

`docker compose build` builds the containers using the docker compose file.

`docker compose up` starts the containers using the docker compose file.

## pgcli

`pgcli --help` provides menu the pgcli command variables

    pgcli -h localhost -p 5432 -U root -d ny_taxi
  
runs the open database in port XXX


---

## Container commands

`exit` Exits the container

## Python

      import sys
      file = sys.argv[0] # File name
      arg1 = sys.argv[1] # first argument passed

run locally the ingest data script.

      query = """
      SELECT ....
      """

      pd.read_sql(query, con=engine)
loads the query results 

    URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

    python3 ingest_data.py \
      --user=root \
      --password=root \
      --host=localhost \
      --port=5432 \
      --db=ny_taxi \
      --table_name=yellow_taxi_trips \
      --url=${URL}

## General terminal commands
- ls: List of directories and files
- pwd: Outputs the present working dir
- jupyter nbconvert --to=script notebook.ipynb  : converts the notebook to .py

## other

postgres

`\dt` view all tables

`\d (table name)` describes the shcema of the table

install packages in ubuntu enviroment (mass)

    sudo apt update
    sudo apt install \
      python3-ipykernel \
      python3-pip \
      python3-numpy \
      python3-pandas \
      python3-matplotlib \
      python3-scipy \
      python3-scikit-learn

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet` to download file into directory



