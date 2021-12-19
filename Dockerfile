FROM python:3.9-alpine

COPY . /app
WORKDIR /app

# set environment variables


# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# run
EXPOSE 5000
CMD ["python", "run.py"]
