## Question 1: Context Engineering

Try the following experiment:

1. Open ChatGPT in a private browser window: https://chatgpt.com
2. Enter this prompt: "Create a Kestra flow that loads NYC taxi data from CSV to BigQuery"
3. Then, use Kestra's AI Copilot with the same prompt

After trying the same prompt in ChatGPT vs Kestra's AI Copilot, what is the primary reason AI Copilot generates better Kestra flows?

ChatGPT:
```
id: nyc_taxi_csv_to_bigquery
namespace: company.data

tasks:
  - id: download_csv
    type: io.kestra.plugin.core.http.Download
    uri: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.csv

  - id: upload_to_gcs
    type: io.kestra.plugin.gcp.gcs.Upload
    from: "{{ outputs.download_csv.uri }}"
    bucket: my-data-bucket
    name: nyc-taxi/yellow_tripdata_2024-01.csv

    serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"

  - id: load_to_bigquery
    type: io.kestra.plugin.gcp.bigquery.LoadFromGcs
    projectId: my-gcp-project
    dataset: nyc_taxi
    table: yellow_tripdata

    from:
      - gs://my-data-bucket/nyc-taxi/yellow_tripdata_2024-01.csv

    format: CSV
    autodetect: true
    skipLeadingRows: 1
    writeDisposition: WRITE_TRUNCATE

    serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"
```

AI Copilot:
```
id: nyc_taxi_data_load
namespace: dev.kestra.bigquery

tasks:
  - id: download_taxi_data
    type: io.kestra.plugin.core.http.Download
    uri: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.csv
    saveAs: yellow_tripdata_2023-01.csv

  - id: load_to_bigquery
    type: io.kestra.plugin.gcp.bigquery.Load
    # Replace with your actual Google Cloud Project ID, BigQuery Dataset ID, and Table ID
    destinationTable: "your_project_id.your_dataset_id.your_table_id"
    from: "{{ outputs.download_taxi_data.uri }}"
    format: CSV
    csvOptions:
      # Skips the header row in the CSV file
      skipLeadingRows: 1
    # If you need to specify a service account, uncomment and replace with your service account key
    # serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"
```

**Answer:** We can say that AI Copilot has access to current Kestra plugin documentation

---

## Question 2: RAG vs No RAG

Run both `1_chat_without_rag.yaml` and `2_chat_with_rag.yaml` in the Kestra UI. Read the execution logs for each.


non-RAG response:
```
‚ùå Response WITHOUT RAG (no retrieved context):
Kestra 1.1 introduced several exciting features and improvements. Here are 5 major ones:
1. **Event-Driven Flows (Triggers):** This was a significant addition, allowing Kestra workflows to be automatically initiated by external events. Instead of relying solely on scheduled executions or manual starts, users could now define "triggers" that would kick off a flow based on an event occurring in a connected system (e.g., a file appearing in S3, a message in Kafka, a change in a database). This moved Kestra further into being a true event-driven orchestration platform.
2. **Plugin System Improvements (including Python plugins for Workers):** Kestra 1.1 brought notable enhancements to its plugin system, particularly improving the flexibility and power of Python plugins. While Python plugins existed before, this release made it easier to create and manage custom Python tasks, and crucially, allowed Python tasks to run directly on Kestra workers (previously, some Python tasks might have required a Docker container or more complex setup). This streamlined the development of custom Python logic within workflows.
3. **Namespace-Level Defaults:** This feature allowed users to define default configurations at the namespace level. Instead of repeating the same configuration (e.g., Docker image, specific environment variables, retry policies) for every flow within a namespace, they could now set these defaults once. Any flow in that namespace would inherit these settings unless explicitly overridden. This significantly reduced boilerplate code and improved maintainability for larger projects.
4. **Flow Bundles & Blueprints:** Kestra 1.1 introduced the concept of "Flow Bundles" (later often referred to as Blueprints). This allowed users to package and share reusable collections of flows, often accompanied by necessary configurations and documentation. This was a big step towards promoting best practices, accelerating development, and enabling easier sharing of common patterns and solutions across teams or organizations.
5. **Enhanced UI for Debugging & Monitoring:** The Kestra UI received several improvements aimed at making debugging and monitoring of flows more intuitive and powerful. This included better visualizations of flow runs, easier access to logs, and more detailed information about task executions. These UI enhancements were crucial for operators and developers to quickly understand the state of their workflows, identify issues, and troubleshoot effectively.
ü§î Did you notice that this response seems to be:
- Incorrect?
- Vague/generic?
- Listing features that haven't been added in exactly this version but rather a long time ago?
üëâ This is why context matters! Run `2_chat_with_rag.yaml` to see the accurate, context-grounded response.
```

RAG response:
```
‚úÖ RAG Response (with retrieved context):
Kestra 1.1 introduced several major features. Here are at least 5 of them with brief descriptions:
1. **New Filters**: The UI filters across Kestra were completely redesigned based on user feedback to be more intuitive and powerful. Users can now choose from explicit filter options, reset filters with a single click, save frequently used filter combinations, and customize table columns.
2. **No-Code Dashboard Editor**: Kestra 1.1 extended the No-Code Multi-Panel Editor to custom dashboards, allowing users to build and customize dashboards directly from the UI without writing YAML. Users can create data sources, visualizations, and charts using form-based tabs.
3. **Multi-Agent AI Systems**: AI agents in Kestra can now use other AI agents as tools, enabling sophisticated multi-agent orchestration workflows where a primary agent can delegate subtasks to specialized expert agents.
4. **Fix with AI**: This feature provides AI-powered suggestions when task runs fail, helping users quickly diagnose and resolve issues with intelligent recommendations for fixing problems.
5. **Human Task**: For Enterprise Edition users, the new `HumanTask` allows for manual approval steps in workflows. Executions pause at a human task until designated users or group members approve and resume them, enabling human-in-the-loop workflows.
6. **Dozens of New Plugins**: Kestra 1.1 included numerous new plugins contributed by the community, expanding integration capabilities across various categories such as Data & Database (e.g., Liquibase, dlt), SaaS & API (e.g., Airtable, Stripe, Shopify), Cloud & Infrastructure (e.g., Dataform, AWS CloudWatch), and AI Model Providers (e.g., Oracle Cloud Infrastructure GenAI, Cloudflare Workers AI).
üéâ Note that this response is detailed, accurate, and grounded in the actual release documentation. Compare this with the output from 1_chat_without_rag.yaml!
```

**Answer:** The non-RAG response about Kestra 1.1 features is best described as Accurate and specific, matching the actual release notes

---

## Question 3: Token usage ‚Äî short summary

Run `4_simple_agent.yaml` with `summary_length = short` (leave the other inputs as defaults).

Open the execution logs and find the token usage logged by the `log_token_usage` task.

What is the approximate **output** token count for `multilingual_agent`?

`log_token_usage` task:
```
Multilingual Agent:
- Input tokens: 282
- Output tokens: 76
- Total tokens: 358
```

**Answer:** The approximate output token count for multilingual_agent is 60-100 tokens

---

## Question 4: Token usage ‚Äî long summary

Run `4_simple_agent.yaml` again with `summary_length = long`.

Compare the `multilingual_agent` output token count to your result from Question 3. Roughly how many times more output tokens does the long summary use?

`log_token_usage` task:
```
Multilingual Agent:
- Input tokens: 282
- Output tokens: 195
- Total tokens: 477
```

**Answer:** The long summary uses 2-5x more

---

## Question 5: Modifying a flow

Open `4_simple_agent.yaml` in the Kestra flow editor. Find the `english_brevity` task and change its prompt from asking for exactly **1 sentence** to asking for exactly **3 sentences**.

Save the flow, then run it with `summary_length = long`.

Compare the `english_brevity` output token count to the original 1-sentence version (also with `summary_length = long`). How do they compare?

`log_token_usage` task:
```
Multilingual Agent:
- Input tokens: 282
- Output tokens: 169
- Total tokens: 451
```

**Answer:** The output token count to the original 1-sentence version with summary_length = long is 2-4x more.

---

## Question 6: Best Practices

Based on what you learned in this module, for production workflows requiring deterministic, repeatable results with strict compliance requirements (e.g., financial reporting, workflows in highly regulated industries), which approach is most appropriate?

**Answer:** The Use of traditional task-based workflows for predictability and auditability  is the most appropriate approach

