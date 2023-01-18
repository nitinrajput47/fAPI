FROM python:3.9-slim-buster

WORKDIR /fAPI

COPY requirements.txt ./

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8050","--reload"]

