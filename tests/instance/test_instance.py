from coord.instance.schema import InstanceParams
from coord.instance.services import start_instance
from coord.resourcestore import RedisResourceStore


def test_create_instance():
    instance_params = InstanceParams(name='i1ah',
                                     otis_engines=1,
                                     psge_engines=1,
                                     psge_replicas=1)

    resource_store = RedisResourceStore()
    resource_store.set_resources(resource_type="cluster", resources=['AZ1', 'AZ2', 'AZ3'])

    instance = start_instance(instance_params=instance_params,
                               resource_store=resource_store)

    assert instance is not None \
           and instance.instance_params.name == instance_params.name \
           and len(instance.psge_vms) == instance_params.psge_replicas
