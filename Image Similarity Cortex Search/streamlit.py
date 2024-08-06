import streamlit as st # Import python packages
from snowflake.snowpark.context import get_active_session

from snowflake.core import Root

import pandas as pd
import json

pd.set_option("max_colwidth",None)

### Default Values
NUM_CHUNKS = 3 # Num-chunks provided as context. Play with this to check how it affects your accuracy

# service parameters
CORTEX_SEARCH_DATABASE = "DB"
CORTEX_SEARCH_SCHEMA = "SCHEMA"
CORTEX_SEARCH_SERVICE = "DISNEY_SEARCH_SERVICE_CS"
######
######

# columns to query in the service
COLUMNS = [
    "chunk",
    "relative_path",
    "category"
]

session = get_active_session()
root = Root(session)                         

svc = root.databases[CORTEX_SEARCH_DATABASE].schemas[CORTEX_SEARCH_SCHEMA].cortex_search_services[CORTEX_SEARCH_SERVICE]
   
### Functions
     
def config_options():

    categories = session.sql('select "category" from "images_prompts"  where "category" is not null group by "category"').collect()

    cat_list = ['ALL']
    for cat in categories:
        cat_list.append(cat.category)
            
    st.sidebar.selectbox('Select what products you are looking for', cat_list, key = "category_value")

    st.sidebar.expander("Session State").write(st.session_state)

def get_similar_chunks_search_service(query):

    if st.session_state.category_value == "ALL":
        response = svc.search(query, COLUMNS, limit=NUM_CHUNKS)
    else: 
        filter_obj = {"@eq": {"category": st.session_state.category_value} }
        response = svc.search(query, COLUMNS, filter=filter_obj, limit=NUM_CHUNKS)

    st.sidebar.json(response.json())
    
    return response

def create_prompt (myquestion):
    prompt = f"""[0]
     'Question:  
       {myquestion} 
       Answer: '
       """
    relative_paths = "None"
            
    return prompt, relative_paths

def complete(myquestion):

    prompt, relative_paths =create_prompt (myquestion)
    cmd = """
            select snowflake.cortex.complete(?, ?) as response
          """
    
    df_response = session.sql(cmd, params=[st.session_state.model_name, prompt]).collect()
    return df_response, relative_paths

def main():
    
    st.title(f": Prompt to find similar images")
    st.write("This is the list of images that are similar the your prompt questions:")

    config_options()

    # st.session_state.rag = st.sidebar.checkbox('Use your own documents as context?')

    question = st.text_input("Enter question", placeholder="young businessman", label_visibility="collapsed")

    if question:
        response = get_similar_chunks_search_service(question)
        for idx in range(0,len(response.results)):
            st.write('      ')
            st.write(response.results[idx]["chunk"])
            path = response.results[idx]["relative_path"]
            cmd2 = f"select GET_PRESIGNED_URL(@model_stage_similarity, '{path}', 360) as URL_LINK from directory(@model_stage_similarity)"
            df_url_link = session.sql(cmd2).to_pandas()
            url_link = df_url_link._get_value(0,'URL_LINK')
            display_url = f"Image: [{path}]({url_link})"
            st.image(url_link)
                
if __name__ == "__main__":
    main()