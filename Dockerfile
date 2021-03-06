FROM python:3.8.0

LABEL maintainer="Aly Sivji <alysivji@gmail.com>" \
    description="StreetTeam -- Development image"

WORKDIR /app

COPY requirements.txt requirements_dev.txt /tmp/

RUN groupadd -g 901 -r sivdev \
    && useradd -g sivdev -r -u 901 sivdev_user \
    && pip install --no-cache-dir -r /tmp/requirements_dev.txt

EXPOSE 8100

# Switch from root user for security
# USER sivdev_user

COPY ./ /app

ENTRYPOINT [ "scripts/entrypoint.sh" ]
