import os
from typing import List
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
from google.protobuf.json_format import MessageToDict
from dotenv import load_dotenv

load_dotenv()
GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
AGENT_ID = os.environ["AGENT_ID"]
APP_LOCATION = os.environ["APP_LOCATION"]

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sa.json"


def get_vertex_ai_search_config():
    client_options = (
        ClientOptions(api_endpoint=f"{APP_LOCATION}-discoveryengine.googleapis.com")
        if APP_LOCATION != "global"
        else None
    )

    client = discoveryengine.SearchServiceClient(client_options=client_options)
    serving_config = (
        f"projects/{GCP_PROJECT_ID}/locations/{APP_LOCATION}"
        f"/collections/default_collection/engines/{AGENT_ID}"
        f"/servingConfigs/default_config"
    )

    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            summary_result_count=5,
            include_citations=True,
            ignore_adversarial_query=True,
            ignore_non_summary_seeking_query=True,
            model_prompt_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec(
                preamble="Summary the NAV the fund detail and provide recommendation based on YTD value provide knowledge about each Fund in Thai"
            ),
            model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(
                version="stable",
            ),
        ),
    )
    return client, serving_config, content_search_spec


def search_ai(query):
    # Search Configuration
    client, serving_config, content_search_spec = get_vertex_ai_search_config()

    search_query = query
    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=5,
        content_search_spec=content_search_spec,
        query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
            condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
        ),
        spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
            mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
        ),
    )

    response = client.search(request)
    response_dict = MessageToDict(response._pb)

    gemini_summary_text = response_dict["summary"]["summaryText"]
    search_results = response_dict["results"]
    return gemini_summary_text, search_results