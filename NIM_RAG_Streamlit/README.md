# RAG on SNOWFLAKE SPCS and NVIDIA MICROSERVICE 

This implementation is tied to the [YouTube video on NVIDIA Developer](https://youtu.be/N_OOfkEWcOk) and the [repo](https://github.com/NVIDIA/GenerativeAIExamples/blob/105422558ed968a4dfc4ef6cbebc673cf42a00de/community/5_mins_rag_no_gpu/README.md)

This is a simple standalone implementation showing a minimal RAG pipeline that uses models available from [NVIDIA API Catalog](https://catalog.ngc.nvidia.com/ai-foundation-models).
The catalog enables you to experience state-of-the-art LLMs accelerated by NVIDIA.
Developers get free credits for 10K requests to any of the models.

The example uses an [integration package to LangChain](https://python.langchain.com/docs/integrations/providers/nvidia) to access the models.
NVIDIA engineers develop, test, and maintain the open source integration.
This example uses a simple [Streamlit](https://streamlit.io/) based user interface and has a one-file implementation.
Because the example uses the models from the NVIDIA API Catalog, you do not need a GPU to run the example.

### Steps to implement NVIDIA RAG on SPCS

1. Create snowflake image repository using [setup.sql](https://github.com/sfc-gh-knadadur/snowpark-use-cases/blob/main/NIM_RAG_Streamlit/snowflake/01%20Setup.sql). Use snowflake worksheet


2. Update [docker steps](https://github.com/sfc-gh-knadadur/snowpark-use-cases/blob/main/NIM_RAG_Streamlit/docker/Docker_Setup) the Snowflake Image repository URL and 


3. Run [docker steps](https://github.com/sfc-gh-knadadur/snowpark-use-cases/blob/main/NIM_RAG_Streamlit/docker/Docker_Setup) to build the streamlit docker image and install the requirements: On your CLI


   If you don't already have an API key, visit the [NVIDIA API Catalog](https://build.ngc.nvidia.com/explore/), select on any model, then click on `Get API Key`.

3. Update the API Key in the [SPCS spec yaml](https://github.com/sfc-gh-knadadur/snowpark-use-cases/blob/main/NIM_RAG_Streamlit/snowflake/SPCS%20spec/NIMS_RAG_mistral_streamlit_rag.yaml)

   ```console
         env:
        NVIDIA_API_KEY: "nvapi-APIKEY"
   ```

4.  Upload the yaml file to snowflake stage SPEC (created in step 1)

5. [Create Service and validate ](https://github.com/sfc-gh-knadadur/snowpark-use-cases/blob/main/NIM_RAG_Streamlit/snowflake/02%20Create_Service.sql)


6. Test the deployed example by going to `ingress url` from the endpoint in a web browser.

   Click **Browse Files** and select your knowledge source.
   After selecting, click **Upload!** to complete the ingestion process.

You are all set now! Try out queries related to the knowledge base using text from the user interface.
