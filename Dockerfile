# Using a base image:
FROM continuumio/miniconda3
# Update conda:
RUN conda update -n base -c defaults conda
# Create the environment:
COPY langchain_ai.yml .
COPY notebooks ./notebooks
RUN conda env create -f langchain_ai.yml
WORKDIR /home
EXPOSE 8080
ENTRYPOINT ["conda", "run", "-n", "langchain_ai", "jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
