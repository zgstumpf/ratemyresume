# Get Anaconda
FROM continuumio/miniconda3

COPY environment.yaml /tmp/environment.yaml

# Create conda environment from .yml file
RUN conda env create --file /tmp/environment.yaml

# Set path to newly created conda environment - name is hardcoded here
ENV PATH=/opt/conda/envs/ratemyresume/bin:$PATH

# Send Python outputs to terminal or container log
ENV PYTHONUNBUFFERED=1

# Install LibreOffice, which is used to convert files to pdf
RUN apt update && apt install libreoffice -y

RUN mkdir /ratemyresume
WORKDIR /ratemyresume
ADD . /ratemyresume/

EXPOSE 8000