FROM python:3.9.5

# streamlit need the port 8501 to be exposed
EXPOSE 8501

# set up location of code
WORKDIR /opt/sde/src/streamlit_app

# lets us import from folders inside /src/loader directly
ENV PYTHONPATH=/opt/sde

# install python requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# COPY our code folder to docker
COPY ../.. /opt/sde

# keep our docker container running
CMD ["tail", "-f", "/dev/null"]
