import argparse
import json

from environs import Env
from google.cloud import dialogflow

env = Env()
env.read_env()


def create_intent(
    project_id,
    display_name,
    training_phrases_parts,
    message_texts
):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def main():
    google_project_id = env.str('GOOGLE_PROJECT_ID')
    parser = argparse.ArgumentParser('Create intents from json file')
    parser.add_argument('path', help='Path to json file')
    args = parser.parse_args()

    with open(args.path, 'r', encoding='utf-8') as json_file:
        intents = json.load(json_file)

    for intent_name, intent in intents.items():
        questions = intent['questions']
        answer = [intent['answer'], ]
        create_intent(
            google_project_id,
            intent_name,
            questions,
            answer
        )


if __name__ == '__main__':
    main()
