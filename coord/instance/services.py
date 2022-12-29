import logging
import os
from typing import List

import docker

from coord.instance.schema import InstanceParams, Instance, InstanceContainer
from coord.resourcestore import ResourceStore
from ssh import ssh

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def allocate_instance(instance_params: InstanceParams, resource_store: ResourceStore) -> Instance:
    # TODO Find root location
    root_folder = '/'

    how_many = instance_params.psge_replicas + 1
    vms = resource_store.allocate_resource(resource_type="cluster", how_many=how_many, reason=instance_params.name)
    instance = None
    if len(vms) > 1:
        instance = Instance(instance_params=instance_params,
                            root_folder=root_folder,
                            otis_url=vms[0],
                            otis_vms=[vms[0]],
                            dash_vms=[vms[0]],
                            psge_vms=vms[1:])

    return instance


def instance_status(instance: Instance):
    vms = set()
    vms.update(instance.otis_vms, instance.dash_vms, instance.psge_vms)

    containers = []
    for vm in vms:
        client = docker.DockerClient(base_url='ssh://andrewwi@desktop-tthtjf3',
                                     use_ssh_client=False)
        for c in client.containers.list():
            if instance.instance_params.name in c.attrs['Name']:
                containers.append(InstanceContainer(host_name=vm,
                                                    container_name=c.attrs['Name']))

    instance.containers = containers


def ssh_multiple(vms: List[str], user: str, cmd: str):
    for vm in vms:
        logger.info('SSH {vm} {user} {cmd}')
        ssh('desktop-tthtjf3', 'andrewwi', cmd)


def start_services(instance: Instance):
    ssh_multiple(instance.otis_vms, os.getlogin(), get_cmd(instance, 'otis'))
    ssh_multiple(instance.dash_vms, os.getlogin(), get_cmd(instance, 'dash'))
    ssh_multiple(instance.psge_vms, os.getlogin(), get_cmd(instance, 'psge'))


def get_cmd(instance: Instance, component: str):
    container_name = f'{instance.instance_params.name}_{component}'
    cmd = f'docker rm -f {container_name} & docker run -d --name {container_name} sito'
    return cmd


def start_instance(instance_params: InstanceParams, resource_store: ResourceStore) -> Instance:
    # TODO Find if instance allocated already !

    instance = allocate_instance(instance_params, resource_store)
    start_services(instance)
    instance_status(instance)
    return instance
