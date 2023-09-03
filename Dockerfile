FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt

EXPOSE 8000

ENV NAME SimpleQ

CMD ["uvicorn", "src.API.main:app", "--reload"]
