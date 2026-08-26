#!/bin/bash
set -e

docker-entrypoint.sh mariadbd &
mariadb_pid=$!

echo "[catvault] waiting for mariadb..."
until mariadb -h 127.0.0.1 -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE" \
        -e 'SELECT 1;' >/dev/null 2>&1; do
    if ! kill -0 "$mariadb_pid" 2>/dev/null; then
        echo "[catvault] mariadb exited during startup" >&2
        wait "$mariadb_pid"
        exit 1
    fi
    sleep 1
done

if [ -e /flag.txt ]; then
    chown root:root /flag.txt 2>/dev/null || echo "[catvault] warning: could not chown /flag.txt" >&2
    chmod 0400 /flag.txt 2>/dev/null || echo "[catvault] warning: could not chmod /flag.txt (read-only mount?)" >&2
else
    echo "[catvault] warning: /flag.txt is not mounted" >&2
fi

echo "[catvault] meowing"

exec gosu catvault /opt/venv/bin/python3 app.py
