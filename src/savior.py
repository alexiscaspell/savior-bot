import requests as req
from typing import List
from src.app_model import AppModel

class Service(AppModel):
    id: str = None
    name: str = None

class Consequence(AppModel):
    action: str
    result: object

class ResultRule(AppModel):
    name: str
    consequences: List[Consequence]

class PrayResponse(AppModel):
    service: str
    rules: List[ResultRule]

class Savior():
    def __init__(self,url):
        self.url = url

    def get_by_name_like(self,name:str):
        response = req.get(f"{self.url}/services?name={name}").json()
        return [Service.from_dict(s) for s in response]
    def pray(self,id:str):
        response = req.get(f"{self.url}/savior/pray/service/{id}").json()
        return PrayResponse.from_dict(response)

        
