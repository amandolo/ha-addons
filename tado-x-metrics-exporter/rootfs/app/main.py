from os import environ, remove
from time import sleep
from prometheus_client import start_http_server, Gauge

from PyTado.interface.interface import Tado

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    username = environ["TADO_USERNAME"]
    password = environ["TADO_PASSWORD"]
    exporter_port = int(environ.get("TADO_EXPORTER_PORT", 8989))
    refresh_rate = int(environ.get("TADO_EXPORTER_REFRESH_RATE", 60))
    token_file_path = environ.get("TADO_TOKEN_FILE_PATH", "/data/oauth_refresh_token")

    print("Starting tado exporter")
    start_http_server(exporter_port)

    temp = Gauge('tado_sensor_temperature_value', 'Temperature as read by the sensor',
                 labelnames=['zone'],
                 unit='celsius')
    temp_setting = Gauge('tado_setting_temperature_value', 'Temperature configured in the zone',
                 labelnames=['zone'],
                 unit='celsius')
    humi = Gauge('tado_sensor_humidity_percentage', 'Humidity as read by the sensor',
                 labelnames=['zone'],
                 unit='percentage')
    heat = Gauge('tado_activity_heating_power_percentage', 'Heating power',
                 labelnames=['zone'],
                 unit='percentage')

    print("Exporter ready")
    print("Connecting to tado API using account " + username)

    while True:
        try:
            tado = Tado(token_file_path=token_file_path)
            status = tado.device_activation_status()
            if status == "NOT_STARTED":
                remove(token_file_path)
                tado = Tado(token_file_path=token_file_path)
                status = tado.device_activation_status()
            if status == "PENDING":
                url = tado.device_verification_url()
                print("Please complete login at URL: " + url)
                tado.device_activation()
                status = tado.device_activation_status()
            if status == "COMPLETED":
                print("Login successful / refreshed")
            else:
                print(f"Login status is {status}")
        except KeyError:
            print("Authentication failed. Check your username, password or client secret.")
            exit(1)

        try:
            for zone in tado.get_zone_states():
                temp.labels(str(zone['name'])).set(zone['sensorDataPoints']['insideTemperature']['value'])
                temp_setting.labels(str(zone['name'])).set(zone['setting']['temperature']['value'] if zone['setting']['temperature'] else 0)
                humi.labels(str(zone['name'])).set(zone['sensorDataPoints']['humidity']['percentage'])
                heat.labels(str(zone['name'])).set(zone['heatingPower']['percentage'])
        except:
            print("Cannot read data from Tado API. Will retry later.")
        finally:
            # TODO: implement a drift-free loop
            sleep(refresh_rate)
