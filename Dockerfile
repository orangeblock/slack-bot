FROM python:2.7-slim
ADD . /src
WORKDIR /src
RUN apt-get update && apt-get install -y gcc libxml2-dev libxslt1-dev python-dev zlib1g-dev
RUN pip install -r requirements.txt
CMD python ./src/app.py
