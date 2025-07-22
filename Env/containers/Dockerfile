# use .env variables in a Dockerfile

FROM postgres:15

# Reference .env via ARG in Dockerfile
# ARG must be declared before using them as ENV

ARG WRITER_EXPOSE_PORT
ARG READER_EXPOSE_PORT

ENV WRITER_PORT=${WRITER_EXPOSE_PORT}
ENV READER_PORT=${READER_EXPOSE_PORT}

RUN echo 'Exposing ports...' \
    && echo "Exposed ports: $WRITER_PORT, $READER_PORT"
