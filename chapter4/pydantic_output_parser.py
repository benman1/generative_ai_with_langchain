from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional


class PlanItem(BaseModel):
    step: str
    tools: Optional[str] = []
    data_sources: Optional[str] = []
    sub_steps_needed: str

class Plan(BaseModel):
    plan: List[PlanItem]


parser = PydanticOutputParser(pydantic_object=Plan)
parser.get_format_instructions()
