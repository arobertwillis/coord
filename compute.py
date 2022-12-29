from coord.instance.schema import InstanceParams, Instance


class ClusterState:

    def allocate_vm(self, reason):
        pass

    def free_vm(self, vm: str):
        pass


class Executor:

    def start(self, vm: str, script: str):
        pass

    def get_containers(self, vm: str):
        pass

    def stop(self, vm: str, script: str):
        pass


class ContainerService:

    def start(self, instance_parms: InstanceParams):
        pass

    def get(self, instance_params: InstanceParams):
        pass

    def stop(self, instance_parms: InstanceParams):
        pass
