import abc
from typing import Iterable


class ResourceStore(abc.ABC):

    @abc.abstractmethod
    def set_resources(self, resource_type: str, resources: Iterable[str]):
        pass

    @abc.abstractmethod
    def allocate_resource(self, resource_type, how_many: int, reason: str):
        pass

    @abc.abstractmethod
    def get_resources(self, resource_type, reason: str) -> Iterable[str]:
        pass

    @abc.abstractmethod
    def free_resources(self, resource_type, reason) -> Iterable[str]:
        pass


import redis

r = redis.Redis()


class RedisResourceStore(ResourceStore):
    def allocate_resource(self, resource_type, how_many: int, reason: str):
        resources = r.spop(resource_type, how_many)
        r.sadd(reason, *resources)
        return resources

    def get_resources(self, name: str) -> Iterable[str]:
        return r.smembers(name)

    def free_resources(self, resource_type, reason) -> Iterable[str]:
        resources = r.smembers(reason)
        if len(resources) > 0:
            r.sadd(resource_type, *resources)
        r.delete(reason)

    def set_resources(self, resource_type: str, resources: Iterable[str]):
        r.delete(resource_type)
        r.sadd(resource_type, *resources)


def get_resource_store():
    resource_store = RedisResourceStore()
    resource_store.set_resources(resource_type="cluster", resources=['az1', 'az2', 'az3'])

    try:
        yield resource_store
    finally:
        pass

if __name__ == "__main__":

    redis_store = RedisResourceStore()

    redis_store.set_resources(resource_type="cluster", resources=['az1', 'az2', 'az3'])
    redis_store.free_resources("cluster",'i1ah')
    print(redis_store.get_resources("cluster"))
    print(redis_store.allocate_resource("cluster", 1,'i1ah'))
    print(redis_store.get_resources("cluster"))
    print(redis_store.get_resources("i1ah"))
