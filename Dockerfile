FROM python:3.11-alpine

WORKDIR /app

RUN pip3 install --upgrade pip

COPY requirements.txt /app

RUN apk add --no-cache tesseract-ocr python3 py3-numpy && \
    pip3 install --upgrade pip setuptools wheel && \
    apk add --no-cache --virtual .build-deps gcc g++ zlib-dev make python3-dev py3-numpy-dev jpeg-dev && \
    pip3 install matplotlib && \
    apk del .build-deps

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

ENTRYPOINT ["python3"]

CMD ["main.py"]