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
from langchain import LLMChain, PromptTemplate
from langchain.chains.base import Chain
from langchain.llms import FakeListLLM
from langchain.tools.python.tool import sanitize_input
from pip._internal.exceptions import InstallationError
from pydantic import BaseModel, Field

logging.basicConfig(encoding="utf-8", level=logging.INFO)
DEV_PROMPT = (
    "You are a software engineer who writes Python code given tasks or objectives. "
    "Come up with a python code for this task: {task}"
    "Please use PEP8 syntax and comments!"
)


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


class PythonDeveloper:
    """Execution environment for Python code."""

    def __init__(
            self,
            llm_chain: Chain,
            path: str = "dev",
            audit_file: str = "audit.log",
            do_sanitize_input: bool = True,
            save_intermediate_steps: bool = False
    ):
        self.save_intermediate_steps = save_intermediate_steps
        self.llm_chain = llm_chain
        self.path = path
        self.create_directory()
        self.logger = logging.getLogger()
        self.logger.addHandler(
            self.setup_audit_trail(audit_file=audit_file)
        )
        self.do_sanitize_input = do_sanitize_input

    def write_code(self, task: str) -> str:
        """Given a task description write Python code.

        If intermediate steps are desired, store the code to
        a separate Python file.
        """
        code = self.llm_chain.run(task)
        if self.save_intermediate_steps:
            self.write_file("", code, "w")
        return code

    @staticmethod
    def setup_audit_trail(audit_file: str) -> FileHandler:
        """Set up a logger that tracks all calls to run."""
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        file_handler = logging.FileHandler(audit_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        return file_handler

    def install_package(
            self,
            module_not_found_error: ModuleNotFoundError
    ) -> bool:
        """Install a package.

        Returns True if installation successful.
        Note: We could implement a logic for virtual environments here.
        """
        try:
            package = str(module_not_found_error).strip().split(" ")[-1].strip("'")
            self.logger.info(f"installing {package}")
            pip.main(['install', package])
            return True
        except InstallationError as ex:
            # Any other error, we want to fail here.
            self.logger.exception(ex)
            return False

    @meaningful_output
    def run(
            self,
            task: str,
            filename: str = "main.py",
            mode: Literal["w", "a"] = "w"
    ) -> str:
        """Generate and execute Python code.

        Returns the output from the run.
        """
        self.logger.info(f"Task:\n{task}")
        code = self.write_code(task)
        self.logger.info(f"Code:\n{code}")
        if self.do_sanitize_input:
            code = sanitize_input(code)

        self.write_file(code=code, filename=filename, mode=mode)
        # import executor; we can try others like pylint
        try:
            # with DirectorySandbox(self.path):
            return self.execute_code(code, filename)
        except (ModuleNotFoundError, NameError) as ex:
            return str(ex)
        except SyntaxError as ex:
            return f"This is not valid Python code! Exception thrown: {ex}"
        except FileNotFoundError as ex:
            # If this is an image, we could add a tool to create images.
            return f"This file doesn't exist!\n{ex}"
        except SystemExit as ex:
            self.logger.warning(ex)
            return str(ex)

    def execute_code(self, code: str, filename: str) -> str:
        """Execute a python code."""
        try:
            with set_directory(Path(self.path)):
                ns = dict(__file__=filename, __name__="__main__")
                function = compile(code, "<>", "exec")
                with redirect_stdout(io.StringIO()) as f:
                    exec(function, ns)
                    return f.getvalue()
        except ModuleNotFoundError as ex:
            if self.install_package(ex):
                return self.execute_code(code, filename)
            raise ex

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
    software_prompt = PromptTemplate.from_template(DEV_PROMPT)
    # careful: if you have the wrong model spec, you might not get any code!
    software_llm = LLMChain(
        llm=FakeListLLM(
            responses=[
                "import os; print(os.getcwd())",
                "import os; os.listdir('.')",
                "print('hello world!')"
            ]
        ),
        prompt=software_prompt
    )
    env = PythonDeveloper(software_llm)
