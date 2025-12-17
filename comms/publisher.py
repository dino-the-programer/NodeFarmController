from github import Github
from pydantic import BaseModel

class DomainEndPoint(BaseModel):
    url:str
    active:bool

def publish(token:str,data:DomainEndPoint=DomainEndPoint(url='',active=False)):
    g = Github(token)
    repo = g.get_repo("dino-the-programer/NodeFarmUrlEndPoint")
    file_path = "data.json"
    commit_message = "."
    branch_name = "main"
    try:
        contents = repo.get_contents(file_path, ref=branch_name)
        repo.update_file(contents.path, commit_message, data.model_dump_json(), contents.sha, branch=branch_name)
        print(f"File '{file_path}' updated successfully.")
    except Exception as e:
        print(f"Could not update file: {e}")