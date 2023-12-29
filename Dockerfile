# Using a base image:
FROM ubuntu:20.04

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
ENV PIP_DEFAULT_TIMEOUT=1000

RUN apt-get update && apt-get install -y wget build-essential && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

RUN conda update -n base -c defaults conda -y && conda --version

# Update the environment:
COPY langchain_ai.yaml .
COPY notebooks ./notebooks
RUN conda env update --name base --file langchain_ai.yaml -vv

WORKDIR /home

EXPOSE 8888
ENTRYPOINT ["conda", "run", "-n", "base", "jupyter", "notebook", "--notebook-dir=/notebooks", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
