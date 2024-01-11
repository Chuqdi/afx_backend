FROM python:3.11.3-slim

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get update \
  && apt install python3-dev musl-dev -y
RUN apt-get install 'ffmpeg'\
  'libsm6'\
  'libxext6' -y

# docker specific configs for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /code/
WORKDIR /code

COPY pyproject.toml /code/

# print all files in the current directory
RUN ls -la

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
# RUN python -m poetry cache clear pypi --all

RUN python -m poetry export -f requirements.txt -o requirements.txt --without-hashes
RUN python -m pip install -r requirements.txt
# RUN python -m poetry install --no-root

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

