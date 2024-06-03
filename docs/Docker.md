Build Docker image and run container. Add `--build` to rebuild image. `-d` lets you use terminal after command is done but prints output to Docker Desktop.
```sh
docker-compose up -d
```

Create `environment.yaml` file.
```sh
conda env export --no-build | grep -v "^prefix: " > environment.yaml
```

Search http://localhost:8000/ to view web app running from Docker. Terminal output gives a different URL - ignore it.

All Python `print()` statements will print to Docker Desktop > Containers > ratemyresume
 - will print to terminal if `-d` is left out?

Quit server
```sh
docker-compose down
```