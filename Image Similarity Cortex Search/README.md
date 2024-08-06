# Running Video Impanting Multi Modal in Snowpark Container Services
This is an art of possibility for setting up and running Video Impanting Multi Modal in inside Snowpark Conatiner Services using GPUs. Download the entire zip and run the docker commands being inside the folder path(after uzipping).

# Setup

## Common Setup
Run the following steps as `ACCOUNTADMIN`.
1. Create a `ROLE` that will be used for Snowpark Container Services administration.
```sql
use role accountadmin;
CREATE ROLE spcs_role;
GRANT ROLE spcs_role TO ACCOUNTADMIN;
GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO ROLE spcs_role;
```
2. Create a `COMPUTE POOL`.
```sql
use role accountadmin;
CREATE COMPUTE POOL compute_pool_gpu_S
MIN_NODES = 1 
MAX_NODES = 1 
INSTANCE_FAMILY = GPU_NV_S
AUTO_RESUME = FALSE;

GRANT USAGE, MONITOR ON COMPUTE POOL compute_pool_gpu_S TO ROLE spcs_role;
3. Create a `WAREHOUSE` that we'll use in our `SERVICE`.
```sql
use role accountadmin;
CREATE OR REPLACE WAREHOUSE wh_xs WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 180
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = FALSE;
GRANT ALL ON WAREHOUSE wh_xs TO ROLE spcs_role;
```
4. Create External Access Integration
```sql
use role accountadmin;

CREATE NETWORK RULE allow_all_rule
    TYPE = 'HOST_PORT'
    MODE= 'EGRESS'
    VALUE_LIST = ('0.0.0.0:443','0.0.0.0:80');

CREATE EXTERNAL ACCESS INTEGRATION allow_all_eai
  ALLOWED_NETWORK_RULES = (allow_all_rule)
  ENABLED = true

GRANT USAGE ON INTEGRATION allow_all_eai TO ROLE SPCS_ROLE;

GRANT ROLE SPCS_ROLE TO USER <user_name>;

```

## Project Setup
1. Use the `SPCS_ROLE`
```sql
USE ROLE spcs_role;
```
2. Create a `DATABASE` and `SCHEMA` for this use. You can, of course use
  an existing `DATABASE` and `SCHEMA`.
```sql
CREATE DATABASE multimodal;
CREATE SCHEMA spcs;
USE SCHEMA multimodal.spcs;
```
3. Create the `IMAGE REPOSITORY` and `STAGES` we will need. 
  Upload the imagesimilarity.yaml to specs stage
```sql
CREATE IMAGE REPOSITORY image_repo;

CREATE OR REPLACE STAGE specs 
    DIRECTORY = ( ENABLE = true ) 
    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );

CREATE OR REPLACE STAGE model_stage_similarity 
    DIRECTORY = ( ENABLE = true ) 
    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );

```
4. You will need the repository URL for the `IMAGE REPOSITORY`. Run
  the following command and note the value for `repository_url`.
```sql
SHOW IMAGE REPOSITORIES;
```

## Build the Docker image and upload to Snowflake
1. In the root directory of this repository, run the following command.

```bash
  docker build --platform linux/amd64 -t imagesimilarity .
 ``` 
2. Tag the image 
```bash
docker tag imagesimilarity:latest  <repository_url>/imagesimilarity:latest

Run SHOW IMAGE REPOSITORIES IN SCHEMA to get the repository URL
```
3. Push the images to Snowflake image repository. 
You can get <b>image_registry_url</b> from the <repository_url>. The value for image registry url will be like orgname-accountname.registry.snowflakecomputing.com
```bash
docker login <image_registry_url> -u <username>

docker push  <repository_url>/imagesimilarity:latest

```

## Create the Service and Grant Access
1. Use the `SPCS_ROLE` and the `DATABASE` and `SCHEMA` we created earlier.
```sql
USE ROLE spcs_role;
USE SCHEMA multimodal.spcs;
```
2. Run the below command to create the service:
```sql
create service imagesimilarity
    in compute pool compute_pool_gpu_S
    from @specs
    specification_file='imagesimilarity.yaml'
    external_access_integrations = (ALLOW_ALL_EAI);
```

3. See that the service has started by executing `SHOW SERVICES IN COMPUTE POOL compute_pool_gpu_S` 
  and `SELECT system$get_service_status('imagesimilarity')`.
4. Find the public endpoint for the service by executing `SHOW ENDP OINTS IN SERVICE imagesimilarity`.


## Use Jupyter-Lab
1. Navigate to the endpoint and authenticate with a user that has access.

2. Navigate to the folder /app/imagesimilarity/imagesimilarity/imagesimilarity-master 

3. Upload the Demo_Notebook.ipynb to the /app/imagesimilarity/imagesimilarity/imagesimilarity-master
Please Note : This has to be direct upload to the folder location. And this is a one time copy and you don't have to perform this again. If you suspend the service, the changes to the notebook will be persisted.

CORTEX_SEARCH_AS_SERVICE is a PubPr feature[Aug 2024] and can be used to create search service on your snowflake table. Check the Demo_Notebook.ipynb to find out how to create the cortex search service.
4. Run this command `ALTER STAGE MODEL_STAGE_SIMILARITY REFRESH;` on snowflake worksheet to make sure the images loaded to the internal stage is refreshed.
5. Copy the streamlit.py script into a Streamlit in Snowflake to create the app.
  a. Import Snowflake package while creating the app
  b. Copy the steamlit.py script
  c. Update the CORTEX_SEARCH_DATABASE
  d. Update the CORTEX_SEARCH_SCHEMA
  e. Run the App

