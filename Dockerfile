# Using a base image:
FROM continuumio/miniconda3


# Update the environment:
COPY langchain_ai.yaml .
COPY notebooks ./notebooks
RUN conda env update --name base --file langchain_ai.yaml

WORKDIR /home

EXPOSE 8080
ENTRYPOINT ["conda", "run", "-n", "langchain_ai", "jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
