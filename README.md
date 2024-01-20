# Data Collection & Human-Feedback-Platform
Easily Collect Data and feedback from humans for Large Language Models

# Run Locally

> Make sure docker is installed

1. Run the mongodb and fastapi

```sh
docker compose up -d
```

2. edit etc hosts

```sh
sudo vim /etc/hosts
```

In the line where `127.0.0.1` is present add the following hosts in the same line - `if-mongo1 if-mongo2 if-mongo3`

3. Check is all the service running
```sh
docker ps -a
```
