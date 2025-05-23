#!/usr/bin/with-contenv bashio

export TADO_USERNAME=$(bashio::config 'tado_username')
export TADO_PASSWORD=$(bashio::config 'tado_password')
export TADO_TOKEN_FILE_PATH=$(bashio::config 'tado_token_file_path')
export TADO_EXPORTER_PORT=$(bashio::addon.port 8989)
export TADO_EXPORTER_REFRESH_RATE=$(bashio::config 'tado_exporter_refresh_rate')

exec python3 /app/main.py