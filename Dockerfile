FROM python:3.9

##RUN apt-get update && apt-get install -y \
  ##  build-essential \
    ##libpq-dev \
    ##python3-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5700

CMD ["python", "app.py"]
