Create or refresh `environment.yaml`
```sh
conda env export --no-build | grep -v "^prefix: " > environment.yaml
```