# Get Anaconda
FROM continuumio/miniconda3

# Build prerequisites needed for Python psycopg package (https://www.psycopg.org/docs/install.html#build-prerequisites)
RUN apt-get update && apt-get install build-essential python3-dev libpq-dev -y

COPY environment.yaml /tmp/environment.yaml

# Create conda environment from .yml file
RUN conda env create --file /tmp/environment.yaml

# Set path to newly created conda environment - name is hardcoded here
ENV PATH=/opt/conda/envs/ratemyresume/bin:$PATH

# Send Python outputs to terminal or container log
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1

# Install LibreOffice, which is used to convert files to pdf - This can take a few minutes
RUN apt-get install libreoffice -y

RUN mkdir /ratemyresume
WORKDIR /ratemyresume
ADD . /ratemyresume/

EXPOSE 8000