import os
import csv
import uuid

from bson.objectid import ObjectId

from src.constants.constants import DATASET_UPLOAD_DIR
from src.project.project_model import ProjectModel
from src.db.db_config import db

def total_data(filename: str):
    filepath = os.path.join(DATASET_UPLOAD_DIR, filename)

    with open(filepath, 'r+') as csv_file:
        reader = csv.reader(csv_file, delimiter = ",")
        data = list(reader)
        row_count = len(data)

    print(row_count)
    
    return row_count
def map_datasets_to_recorders(project_id: str):
    project = db.projects.find_one({"_id": ObjectId(project_id)})
    project = ProjectModel(**project)

    dataset_metadata = {
        "project_id": ObjectId(project_id)
    }

    last_csv_idx = 0
    total_records = total_data(project.dataset_name)
    dataset_recorder = []
    print(project.recorder)
    for recorder in project.recorder:
        print(last_csv_idx, total_records, last_csv_idx <= total_records and last_csv_idx % 5 != 0)
        for i in range(5):
            data = {
                "id": str(uuid.uuid4()),
                "idx": last_csv_idx,
                "recorder": recorder["mobile"],
                "status": "RECORD",
                "points": 0
            }
            last_csv_idx += i
            if(last_csv_idx > total_records):
                break


        while(last_csv_idx <= total_records):
            dataset_recorder.append(data)
            last_csv_idx += 1
            
        last_csv_idx += 1

    dataset_metadata["data"] = dataset_recorder
    print(dataset_metadata)
    db["datasets"].insert_one(dataset_metadata)

"""
status: {
    "0" - RECORD
    "1" - REVIEW
    "2" - ACCEPTED
    "3" - REJECTED
}

{
    project_id: ,
    data: [
        {
            id: <UUID>,
            idx: <dataset_idx>,
            recorder: <recorder_no>,
            status: <STATUS>
            points: number
        }
    ]
    
}

"""
