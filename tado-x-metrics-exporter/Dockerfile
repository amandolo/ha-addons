ARG BUILD_FROM
FROM $BUILD_FROM

ARG TEMPIO_VERSION BUILD_ARCH
RUN curl -sSLf -o /usr/bin/tempio "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

ENV PYTHONUNBUFFERED=1

COPY rootfs /

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD [ "/app/run.sh" ]