from typing import List, Dict, Union

from docker.models.containers import Container
from pydantic import BaseModel, Field


class InstanceParams(BaseModel):
    name: str
    otis_engines: int = Field(gt=0)
    psge_engines: int = Field(gt=0)
    psge_replicas: int = Field(gt=0)


class InstanceContainer(BaseModel):
    host_name: str
    container_name: str


class Instance(BaseModel):
    instance_params: InstanceParams
    root_folder: str
    otis_url: str
    otis_vms: List[str]
    dash_vms: List[str]
    psge_vms: List[str]
    containers: Union[List[InstanceContainer],None]
