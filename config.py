snowflake_user = "SNOWGPT"
snowflake_password = "SnowGPT@202308"
snowflake_account = "anblicksorg_aws.us-east-1"
snowflake_warehouse = "SNOWGPT_WH"
snowflake_database = "SNOWGPT_DB"
snowflake_schema = "STG"
stage_name = "snowgpt_s3_stage"

query = "SELECT DISTINCT GET_PRESIGNED_URL(@snowgpt_s3_stage, METADATA$FILENAME) FROM @snowgpt_s3_stage"

api_key = "741d647c-da49-4048-9d88-3b56e9e8e7f3"
environment = "gcp-starter"

index_name="snowpineidx"

openai_api_key="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"