# Home Assistant Add-on: Tado X Exporter

A simple Prometheus exporter for Tado X heating systems. This add-on allows you to monitor your Tado heating system's metrics in Prometheus.

## Installation

1. Navigate to the Home Assistant Add-on Store
2. Add this repository URL: https://github.com/amandolo/ha-addons and check for updates
3. Find the "Tado X Exporter" add-on and click install

## Configuration

This add-on requires your Tado account credentials to access your heating system data.

Example configuration:

```yaml
TADO_USERNAME: your_tado_email@example.com
TADO_PASSWORD: your_tado_password
TADO_EXPORTER_REFRESH_RATE: 180
```

### Option: `TADO_USERNAME` (required)
Your Tado account email address.

### Option: `TADO_PASSWORD` (required)
Your Tado account password.

### Option: `TADO_EXPORTER_PORT` (optional)
The exporter port. Default: 8989

### Option: `TADO_EXPORTER_REFRESH_RATE` (optional)
How often to refresh data from Tado API, in seconds. Default: 180 (3 minutes)

### Option: `TADO_TOKEN_FILE_PATH` (optional)
The path to save the OAuth2 refresh_token. Default: /data/oauth_refresh_token

## How it works

After starting, the add-on connects to the Tado API and begins collecting metrics from your Tado system.
At the first start you have to complete the OAUTH2 verification, you find the URL in the logs.
It exposes the following metrics:

- `tado_sensor_temperature_value_celsius`: Temperature readings from each zone
- `tado_setting_temperature_value_celsius`: Temperature setting from each zone
- `tado_sensor_humidity_percentage`: Humidity readings from each zone
- `tado_activity_heating_power_percentage`: Heating power percentage for each zone

These metrics are available at `http://add-on-hostname:8989/metrics` for scraping by Prometheus.

## Integration with Prometheus

...
To collect these metrics with Prometheus, add the following to your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'tado'
    static_configs:
      - targets: ['your-home-assistant:8989']
```

## Troubleshooting

- If the add-on fails to start, check your Tado credentials.
- The first login may require verification. The add-on will show a URL in the logs that you need to visit to complete activation.
- For any issues, check the add-on logs for more information.
```