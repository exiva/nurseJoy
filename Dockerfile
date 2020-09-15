FROM python:3.8.5-alpine
RUN apk --no-cache add build-base
RUN apk --no-cache add linux-headers
WORKDIR /app
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app
CMD ["python", "-u", "bot.py"]