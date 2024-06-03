Build Docker image and run container. Add `--build` to rebuild image.
```sh
docker-compose up -d
```

Create `environment.yaml` file.
```sh
conda env export --no-build | grep -v "^prefix: " > environment.yaml
```

Search http://localhost:8000/ to view web app running from Docker. All Python `print()` statements will print to Docker Desktop > Containers > ratemyresume

Quit server
```sh
docker-compose down
```