FROM python:3
RUN mkdir /code
WORKDIR /code
EXPOSE 80
ADD . /code/
RUN pip install -r requirements.txt
CMD ["python", "-u", "Model.py"]