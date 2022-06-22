from google.cloud import dialogflow


def get_response_to_message(
    project_id,
    session_id,
    message,
    language_code='ru_RU',
    allow_fallback=True
):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(
        project_id,
        session_id
    )

    text_input = dialogflow.TextInput(
        text=message,
        language_code=language_code
    )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if response.query_result.intent.is_fallback and not allow_fallback:
        return None

    return response.query_result.fulfillment_text
