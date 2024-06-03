# Get Anaconda
FROM continuumio/miniconda3

COPY environment.yml /tmp/environment.yml

# Create conda environment from .yml file -
RUN conda env create --file /tmp/environment.yml

# Set path to newly created conda environment - name is hardcoded here
ENV PATH=/opt/conda/envs/ratemyresume/bin:$PATH

# Send Python outputs to terminal or container log
ENV PYTHONUNBUFFERED=1


# RUN mkdir /ratemyresume_container
# WORKDIR /ratemyresume_container
# ADD . /ratemyresume_container/