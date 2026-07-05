FROM python:3

WORKDIR /loggum

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /loggum/ .

CMD [ "python", "app.py" ]
