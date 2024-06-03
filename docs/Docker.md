Build Docker image and run container
```sh
docker-compose up --build -d
```

See output from `compose.yaml`
```sh
docker-compose logs web
```

Still figuring out how to see output from `Dockerfile`


Create `environment.yml` file. `--no-build` tells conda to leave out the build hash, which is unique to an operating system. Installing a package on MacOS may produce a build hash that does not work with Linux in Docker, which is why the build hash is excluded.
```sh
conda env export --no-build | grep -v "^prefix: " > environment.yml
```