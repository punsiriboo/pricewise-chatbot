import os
import functions_framework
from dotenv import load_dotenv

from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3 import WebhookHandler
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    FileMessageContent,
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
    ShowLoadingAnimationRequest,
    FlexMessage,
    FlexCarousel
)

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]


configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
line_bot_blob_api = MessagingApiBlob(api_client)

from commons.build_flex_message import data_extract_and_search
from commons.gemini_service import (
    generate_text, 
    image_description, 
    document_description,
    get_price_comparison,
)


@functions_framework.http
def callback(request):
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    line_bot_api.show_loading_animation(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )
    gemini_reponse = generate_text(event.message.text)
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=gemini_reponse)],
        )
    )


@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )

    message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
    prompt = """ I have provided an image of an invoice.
        For each product, perform a Google search focusing on e-commerce platforms available in Thailand and Find at least 3 matching or closely similar products from different stores.
        the result as a JSON object including:
        DataSchema = {
            'product': str,
            'original_price': float,
            'average_price': float,
            'comparison': [
                {
                    'store_name': str,
                    'price_thb': float,
                    'product_link': str,
                }
            ]
        }
    """
    gemini_reponse = get_price_comparison(prompt, message_content)

    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(text=gemini_reponse),
            ],
        )
    )


@handler.add(MessageEvent, message=FileMessageContent)
def handle_file_message(event):

    doc_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
    prompt = """ I have provided an image of an invoice. Extract data for me
    DataSchema = [{
        'product': str,
        'original_price': float}]"""
    gemini_reponse = document_description(prompt, doc_content)
    gemini_summary_text, search_results = data_extract_and_search(gemini_reponse)
    

    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(text=gemini_reponse),
            ],
        )
    )
