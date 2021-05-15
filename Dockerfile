# syntax=docker/dockerfile:1
FROM python:3.8

COPY example/ /app/

WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["python"]
CMD ["app.py"]
