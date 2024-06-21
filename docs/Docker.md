Build Docker container. Run this if you make changes to the `Dockerfile`.
```sh
docker-compose build
```

Run Docker container, building it first if a build doesn't exist.
```sh
docker-compose up
```

To stop the Docker container, kill the terminal, and in a new terminal run:
```sh
docker-compose down
```

You can also stop a Docker container via Docker Desktop.

To "go inside" the Docker container to debug, in a new terminal, run `docker exec -it ratemyresume_web_server /bin/bash`. You can then use terminal commands to navigate the Linux operating system that makes up the container.

When a terminal runs `docker-compose up`, that terminal window becomes *attached* to the container's ouput, and you can't type new commands in the same terminal. If you want to type commands in the same terminal, run `docker-compose up -d`. Note that if you do this, you will only be able to see the container outputs in Docker Desktop.

If `python manage.py runserver` fails, the container may forcefully exit before you get the chance to `exec` into it for debugging. To stop the container from exiting, in `compose.yaml`, set `services.web.command` to `tail -f /dev/null`. After debugging, change the command back.