FROM python:3
RUN mkdir /code
WORKDIR /code
EXPOSE 80
ADD . /code/
RUN pip install -r API/requirements.txt
CMD ["python", "API/manage.py", "runserver", "0.0.0.0:8000"]