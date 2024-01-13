from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectModel(BaseModel):
    project_name: str = Field(alias='projectName')
    admin_name: str
    admin_mobile: str
    recorder: Optional[List[dict]] = None
    reviewer: Optional[List[dict]] = None
    record_point: int
    review_point: int
    dataset_name: Optional[str] = None

