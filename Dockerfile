FROM  python:3.7-alpine

COPY bin/octactl /bin/octactl
COPY octactl.yaml /root/.octactl.yaml

ADD src /app/
COPY Pipfile /app/
WORKDIR /app
ENV PIPENV_PIPFILE=/app/Pipfile

RUN mkdir /lib64 && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2
RUN pip3 install pipenv \
    &&  pipenv install \
    && pipenv lock -r > requirements.txt 

CMD [ "pipenv","run","python3","/app/validate.py" ]