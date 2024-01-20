from pydantic import BaseModel, Field, BeforeValidator
from typing import List, Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class ProjectModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    project_name: str
    admin_name: str
    admin_mobile: str
    recorder: Optional[List[dict]] = None
    reviewer: Optional[List[dict]] = None
    record_point: int
    review_point: int
    dataset_name: Optional[str] = None

