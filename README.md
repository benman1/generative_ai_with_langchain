# Generative AI with LangChain 
Create generative AI apps with LangChain.


## Environment
You can install your local environment with conda (recommended) or pip. The environment configurations for conda and pip are provided. Please note that if you choose pip as you installation tool, you might need additional tweaking.

If you have any problems with the environment, please raise an issue, where you show the error you got. If you feel confident, please go ahead and create a pull request.

### Conda
This is the recommended method for installing dependencies. Please make sure you have [anaconda](https://www.anaconda.com/download) installed.

First create the environment for the book that contains all the dependencies:
```bash
conda env create --file langchain_ai.yaml --force
```

The conda environment is called `langchain_ai`. You can activate it as follows:
```bash
conda activate langchain_ai 
```

### Pip
[Pip](https://pypi.org/project/pip/) is the default dependency management tool in Python. With pip, you should be able to install all the libraries from the requirements file:

```bash
pip install -r requirements.txt
```

### Docker
There's a [docker](https://www.docker.com/) file for the environment as well. It uses the docker environment and starts an ipython notebook. To use it, first build it, and then run it:

```bash
docker build -t new_image .
docker run -it new_image
```

You should be able to find the notebook in your browser at [http://localhost:8080](http://localhost:8080).

### Poetry

Make sure you have [poetry](https://python-poetry.org/) installed. On Linux and MacOS, you should be able to use the requirements file:
```bash
poetry install
```
This should take the `pyproject.toml` file and install all dependencies.

## Contributing

If you find anything amiss with the notebooks or dependencies, please feel free to create a pull request.

If you want to change the conda dependency specification (the yaml file), you can test it like this:
```bash
conda env create --file langchain_ai.yml --force
```

You can update the pip requirements like this:
```bash
pip freeze > requirements.txt
```

Please make sure that you keep these two ways of maintaining dependencies in sync.

Then make sure, you test the notebooks in the new environment to see that they run.
