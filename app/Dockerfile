FROM python:3.13

WORKDIR /app

COPY ./ .

RUN python -m pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "fastapi", "run", "/app/src/dl.py", "--port", "80"]