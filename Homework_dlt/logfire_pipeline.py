import dlt
import requests
import os
from dotenv import load_dotenv

load_dotenv()

READ_TOKEN = os.getenv("LOGFIRE_READ_TOKEN")

@dlt.source
def logfire_source():
    @dlt.resource(name="spans")
    def spans():
        headers = {"Authorization": f"Bearer {READ_TOKEN}"}
        # Logfire query API
        response = requests.get(
            "https://logfire-us.pydantic.dev/v1/query",
            headers=headers,
            params={
                "sql": "SELECT * FROM records LIMIT 1000"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        if response.status_code == 200:
            yield response.json()
    return spans()

pipeline = dlt.pipeline(
    pipeline_name="logfire_pipeline",
    destination="duckdb",
    dataset_name="logfire_data"
)

load_info = pipeline.run(logfire_source())
print(load_info)