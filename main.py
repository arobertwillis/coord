import subprocess

from fastapi import FastAPI
import redis

app = FastAPI()

r = redis.Redis()

from coord.instance import router as instance_router

app.include_router(instance_router.router)


@app.on_event("startup")
async def startup_event():
    pass


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ls/{folder}")
def ls(folder: str):
    #    safe_folder = shlx.quote(folder)

    # Construct the command
    cmd = f'dir {folder}'
    args = ['dir', folder]
    #    args = shlex.split(cmd)
    # Run the command
    result = subprocess.run(args, shell=True, capture_output=True)
    return {"ls": str(result.stdout).replace(r'\r\n', r'\n')}


@app.get("/images")
def images():
    args = ['docker', 'images', '--format', '"{{.Repository}}"']
    #    args = shlex.split(cmd)
    # Run the command
    result = subprocess.run(args, shell=True, capture_output=True)
    for l in str(result.stdout).replace(r'\r\n', r'\n').splitlines():
        print(l)
        r.lpush('images', l)
    return {"ls": str(result.stdout).replace(r'\r\n', r'\n')}
