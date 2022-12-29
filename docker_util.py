
import docker

if __name__ == "__main__":
    # DOCKER_HOST ssh://andrewwi@DESKTOP-TTHTJF3
    client = docker.from_env(use_ssh_client=False)
    for c in client.containers.list():
        print(c.attrs)
    o = client.containers.run("ubuntu:latest", "echo hello world")
    print(o)