# Watcher

## 1. Installation Guide

There are two options to install and run this application: manual setup or building a Docker image. Choose the option that best fits your needs and environment.

### Opção 1: Manual Configuration

1. Set up the virtual environment:
```bash
$ python3.10 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

2. Run the application:
```bash
$ python manage.py run
```

### Option 2: Building a Docker Image of the Application

1. Build the image:

```bash
$ docker build -t watcher .
```

2. Run the application:
```bash
$ docker run watcher python manage.py run
```

## 2. Accessing the Shell Inside the Container

Occasionally, you may need to access the shell directly within your container. Here's how you can do it:

### Bash
```bash
$ docker exec -it CONTAINER_ID sh
```

### Python shell
```bash
$ docker exec -it CONTAINER_ID python3 manage.py shell
```

## 3. Testing the Application

1. Activate the virtual environment:
```bash
$ source .venv/bin/activate
```
2. Test the application:
```bash
$ python manage.py test
```
