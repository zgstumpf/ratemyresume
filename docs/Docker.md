Build Docker image and run container. Add `--build` to rebuild image if you make any changes to `Dockerfile`.
```sh
docker-compose up
```

Search [http://localhost:8000/](http://localhost:8000/) to view web app running from Docker. Terminal output gives a different URL - ignore it.

Quit server
```sh
docker-compose down
```