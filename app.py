import time

import docker
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.background import BackgroundTask

app = Starlette()


@app.route('/', methods=['GET'])
async def index(request):
    # task = BackgroundTask(some_task, arg='123')
    task = BackgroundTask(create_docker_container)
    return JSONResponse({'success': True}, background=task, status_code=200)


def some_task(arg: str):
    time.sleep(20)

    with open('results.txt', 'w') as f:
        f.write(arg)

    time.sleep(20)


def create_docker_container():
    client = docker.from_env()
    client.containers.run('python:3.7', 'echo hello world', detach=True, name='test')


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=9090)
