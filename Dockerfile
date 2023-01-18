FROM python:3.10
RUN mkdir /messaging_api_inside_docker
WORKDIR /messaging_api_inside_docker
ADD . /messaging_api_inside_docker/
RUN pip install -r requirements.txt

EXPOSE 3004
CMD ["python", "run.py"]