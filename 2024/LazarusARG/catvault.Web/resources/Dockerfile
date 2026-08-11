FROM gcc:14 AS readflag
WORKDIR /build
COPY readflag.c .

RUN gcc -static -O2 -o readflag readflag.c

FROM mariadb:12.3.2

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-dev \
        gcc \
        libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"

COPY app.py db.py ./
COPY templates ./templates

RUN useradd --system --no-create-home --shell /usr/sbin/nologin catvault

COPY --from=readflag /build/readflag /usr/local/bin/readflag
RUN chown root:root /usr/local/bin/readflag && chmod 4111 /usr/local/bin/readflag

COPY entrypoint.sh /usr/local/bin/run.sh
RUN chmod +x /usr/local/bin/run.sh

EXPOSE 8080

ENTRYPOINT ["run.sh"]
