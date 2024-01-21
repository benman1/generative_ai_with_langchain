# Using a miniconda base image:
FROM continuumio/miniconda3:latest

ENV PIP_DEFAULT_TIMEOUT=1000

RUN apt-get update && apt-get install -y wget build-essential && rm -rf /var/lib/apt/lists/*
RUN conda update -n base -c defaults conda -y && conda --version

# Update the environment:
COPY langchain_ai.yaml .
COPY notebooks ./notebooks
RUN python -m pip install --upgrade pip && conda clean -a && python -m pip cache purge
RUN conda env update --name base --file langchain_ai.yaml -vv

WORKDIR /home

EXPOSE 8888
ENTRYPOINT ["conda", "run", "-n", "base", "jupyter", "notebook", "--notebook-dir=/notebooks", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
