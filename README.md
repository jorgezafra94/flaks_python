
adding some content

# docker
create image
```
docker build -t IMAGE_NAME
```

how to run this on docker

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```