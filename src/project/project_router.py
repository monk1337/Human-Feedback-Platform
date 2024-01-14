from fastapi import Form, APIRouter, UploadFile, Response, Request
from fastapi.encoders import jsonable_encoder

import json

from src.project.project_model import ProjectModel
from src.project.project_controller import save_project
from src.jwt.jwt import create_access_token
from src.jwt.model import TokenPayload
from src.utils.utils import remove_extra_quotes

router = APIRouter()

@router.post("/new")
async def create_project(file: UploadFile, request: Request, response: Response):
    project = await request.form()
    project = jsonable_encoder(project)
    recorder = json.loads(project["recorder"])
    reviewer = json.loads(project["reviewer"])

    project = ProjectModel(projectName=remove_extra_quotes(project["projectName"]), admin_name=remove_extra_quotes(project["adminName"]), admin_mobile=remove_extra_quotes(project["adminMobile"]), recorder=recorder, reviewer=reviewer, record_point=project["recordPoints"], review_point=project["reviewPoints"])

    project_id = save_project(file, project)

    payload = TokenPayload(mobile=project.admin_mobile, role="admin")
    jwt_token = create_access_token(payload)

    response.set_cookie(key="access_token", value=jwt_token, httponly=True, secure=True, samesite="none")

    return {"message": "Project created successfully", "project_id": project_id}
