from flask import Blueprint
from typing import List
from app.helpers import route as _route

_api = Blueprint("api", __name__)

class BlueprintApi:
    """
    some comment
    """

    def get(self, api_path: str, check_query_args: List[str] = [], *, json=True):
        return _route.get(_api, api_path, check_query_args, json=json)

    def post(self, api_path: str, check_query_args: List[str] = [], *, json=True):
        return _route.post(_api, api_path, check_query_args, json=json)

api = BlueprintApi()