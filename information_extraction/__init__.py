"""Information information_extraction from documents.

The example CV is from https://github.com/xitanggg/open-resume.
"""
from typing import Optional

from langchain.chains import create_extraction_chain_pydantic
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field

from config import set_environment

set_environment()


class Experience(BaseModel):
    # the title doesn't seem to help at all.
    start_date: Optional[str] = Field(description="When the job or study started.")
    end_date: Optional[str] = Field(description="When the job or study ended.")
    description: Optional[str] = Field(description="What the job or study entailed.")
    country: Optional[str] = Field(description="The country of the institution.")


class Study(Experience):
    degree: Optional[str] = Field(description="The degree obtained or expected.")
    institution: Optional[str] = Field(
        description="The university, college, or educational institution visited."
    )
    country: Optional[str] = Field(description="The country of the institution.")
    grade: Optional[str] = Field(description="The grade achieved or expected.")


class WorkExperience(Experience):
    company: str = Field(description="The company name of the work experience.")
    job_title: Optional[str] = Field(description="The job title.")


class Resume(BaseModel):
    first_name: Optional[str] = Field(description="The first name of the person.")
    last_name: Optional[str] = Field(description="The last name of the person.")
    linkedin_url: Optional[str] = Field(
        description="The url of the linkedin profile of the person."
    )
    email_address: Optional[str] = Field(description="The email address of the person.")
    nationality: Optional[str] = Field(description="The nationality of the person.")
    skill: Optional[str] = Field(description="A skill listed or mentioned in a description.")
    study: Optional[Study] = Field(
        description="A study that the person completed or is in progress of completing."
    )
    work_experience: Optional[WorkExperience] = Field(
        description="A work experience of the person."
    )
    hobby: Optional[str] = Field(description="A hobby or recreational activity of the person.")


def parse_cv(pdf_file_path: str) -> str:
    """Parse a resume.
    Not totally sure about the return type: is it list[Resume]?
    """
    pdf_loader = PyPDFLoader(pdf_file_path)
    docs = pdf_loader.load_and_split()
    # please note that function calling is not enabled for all models!
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613")
    chain = create_extraction_chain_pydantic(pydantic_schema=Resume, llm=llm)
    return chain.run(docs)


if __name__ == "__main__":
    print(parse_cv(
        "openresume-resume.pdf"
    ))
