from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder

import os
import shutil
import uuid

from src.db.db_config import db
from src.project.project_model import ProjectModel
from src.constants.constants import DATASET_UPLOAD_DIR
from src.authentication.auth_controller import verify_user_logged_in
from src.authentication.auth_model import UserModel

def save_dataset(file: UploadFile):
    filename = str(uuid.uuid4()) + '_' + file.filename
    filepath = os.path.join(DATASET_UPLOAD_DIR, filename)

    with open(filepath, 'wb+') as upload_file:
        shutil.copyfileobj(file.file, upload_file)
    
    return filename

def save_project(file: UploadFile, project: ProjectModel) -> str:
    # verify_user_logged_in(UserModel(mobile=project.admin_mobile, role="admin"))

    filename = save_dataset(file)
    project.dataset_name = filename

    saved_project = db.projects.insert_one(project.model_dump(by_alias=True, exclude=["id"]))

    return str(saved_project.inserted_id)


