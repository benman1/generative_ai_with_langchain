"""Python Sandbox Developer."""
import io
import logging
import os
import uuid
from contextlib import contextmanager, redirect_stdout
from logging import FileHandler
from pathlib import Path
from typing import Literal

import pip
from langchain import PromptTemplate
from langchain.chains.base import Chain
from langchain.tools.python.tool import sanitize_input
from pydantic import BaseModel, Field


class PythonExecutorInput(BaseModel):
    code: str = Field()

def meaningful_output(func):
    def wrapper(*args, **kwargs):
        func_output = func(*args, **kwargs)
        print(func_output)
        if len(func_output.strip()) > 0:
            return f"The code returned the following:\n" \
                   f"{func_output}"
        else:
            return "The code returned nothing."
    return wrapper


def audit_trail(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            print(f"{arg}\n")
        for key in kwargs:
            print("another keyword arg: %s: %s" % (key, kwargs[key]))
        return func(*args, **kwargs)

    return wrapper


@contextmanager
def set_directory(path: Path):
    """Sets working directory within the context

    Parameters:
        * path (Path): path to directory
    """
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


class PythonDeveloper():
    """Execution environment for Python code."""

    def __init__(
            self,
            llm_chain: Chain,
            path: str = "dev",
            audit_file: str = "audit.log",
            do_sanitize_input: bool = True,
            save_intermediate_steps: bool = True
    ):
        self.save_intermediate_steps = save_intermediate_steps
        self.llm = llm_chain
        self.path = path
        self.create_directory()
        self.logger = logging.getLogger()
        self.logger.addHandler(
            self.setup_audit_trail(audit_file=audit_file)
        )
        self.do_sanitize_input = do_sanitize_input

    def write_code(self, task: str) -> str:
        """Given a task description write Python code."""
        code = self.llm.run(task)
        if self.save_intermediate_steps:
            self.write_file("", code, "w")
        return code

    @staticmethod
    def setup_audit_trail(audit_file: str) -> FileHandler:
        """Set up a logger that tracks all calls to run."""
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler = logging.FileHandler(audit_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        return file_handler

    @audit_trail
    @meaningful_output
    def run(
            self,
            task: str,
            filename: str = "main.py",
            mode: Literal["w", "a"] = "w"
    ) -> str:
        """Run Python code in a sandbox.

        Returns the output from the run.
        """
        print(f"task: {task}\n")
        code = self.write_code(task)
        print(f"code: {code}\n")
        if self.do_sanitize_input:
            code = sanitize_input(code)

        self.write_file(code=code, filename=filename, mode=mode)
        # import executor; we can try others like pylint
        # func = compile(f"eval(\"import {module_name}\")", filename="<>", mode="eval")
        try:
            #with DirectorySandbox(self.path):
            stdout = "module"
            iteration = 0
            while "module" in stdout:
                stdout = self.execute_code(code, filename)
                print(stdout)
                if iteration > 0:
                    package = stdout.strip().split(" ")[-1].strip("'")
                    print(f"installing {package}")
                    pip.main(['install', package])
                iteration = iteration + 1
            return stdout
        except ModuleNotFoundError as ex:
            # we could implement a logic here for virtual environments
            return str(ex)
        except SyntaxError as ex:
            return f"This is not valid Python code! Exception thrown: {ex}"
        except FileNotFoundError as ex:
            # If this is an image, we could add a tool to create images.
            return f"This file doesn't exist!\n{ex}"
        except SystemExit as ex:
            self.logger.debug(ex)
            return str(ex)

    def execute_code(self, code: str, filename: str) -> str:
        """Execute a python code."""
        try:
            with set_directory(Path(self.path)):
                ns = dict(__file__=filename, __name__="__main__")
                code = compile(code, "<>", "exec")
                with redirect_stdout(io.StringIO()) as f:
                    exec(code, ns)
                    return f.getvalue()
        except ModuleNotFoundError as ex:
            # we could implement a logic here for virtual environments
            return str(ex)

    def write_file(
            self,
            filename: str,
            code: str,
            mode: Literal["w", "a"] = "w"
    ) -> Path:
        """Write code to disk.

        If filename is an empty string, write to
        random filename. This can be useful as
        intermediate step.

        Returns the path to the new file.
        """
        if not filename:
            filename = str(uuid.uuid4()) + ".py"
        fullpath = Path(self.path) / filename
        with open(fullpath, mode, encoding="utf-8") as f:
            f.write(code)

        return fullpath

    def create_directory(self):
        """Create a directory for the project."""
        os.makedirs(self.path, exist_ok=True)


if __name__ == "__main__":
    software_prompt = PromptTemplate.from_template(
        "You are a software engineer who writes Python code given tasks or objectives. "
        "Come up with a python code for this task: {task}"
        "Please use PEP8 syntax and comments!"
    )
    # careful: if you have the wrong model spec, you might not get any code!
    software_llm = FakeLLM
    env = PythonDeveloper(software_llm)
    print(env.run("""import os; print(os.getcwd())"""))
    print(env.run("""import os; os.listdir(".")"""))
    print(env.run("""print("hello world!")"""))
