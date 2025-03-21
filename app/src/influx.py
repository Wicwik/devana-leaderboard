import os

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = os.environ["DOCKER_INFLUXDB_INIT_BUCKET"]
org = os.environ["DOCKER_INFLUXDB_INIT_ORG"]
token = os.environ["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"]
# Store the URL of your InfluxDB instance
url="http://influxdb:8086"

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

def get_users_and_hours():
   query_api = client.query_api()
   query = 'from(bucket:"devana-leaderboard")\
   |> range(start: -10m)\
   |> filter(fn:(r) => r._measurement == "gpu")\
   |> filter(fn:(r) => r._field == "used_hour")\' \
   |> filter(fn:(r) => r.host == "devana-leaderboard-telegraf")\
   |> last()'

   result = query_api.query(org=org, query=query)
   # print(result)

   return [{"user": record.values.get("user"), "gpu_time": record.get_value()} for table in result for record in table.records]