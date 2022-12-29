from fastapi import APIRouter, Depends, status

from coord.resourcestore import ResourceStore,get_resource_store
from . import services
from . import schema

router = APIRouter(
    tags=['Instance'],
    prefix='/instance'
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Instance)
def start_instance(instance_params: schema.InstanceParams, resource_store: ResourceStore = Depends(get_resource_store)):
    return services.start_instance(instance_params, resource_store)
