Script created based on https://www.youtube.com/watch?v=AAMJZTEH_h4

## Running

You can run script with docker or python

### Python
```shell
python main.py --config_file src/project_chat/config_sample.toml
```

### Docker

```shell
docker build -t RepoChat .
docker run -it RepoChat /bin/sh
python main.py
```
