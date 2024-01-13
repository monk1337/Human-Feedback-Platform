import os
from src.constants.constants import FOLDERS

class Folder_handler:
    def __init__(self):
        pass
    
    @staticmethod
    def create_folder():
        try:
            for folder in FOLDERS:
                if(not os.path.exists(folder)):
                    os.mkdir(folder)
        except:
            pass
