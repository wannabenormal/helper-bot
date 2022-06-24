import argparse
import json

from environs import Env

from api_google import create_intent


def main():
    env = Env()
    env.read_env()
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
