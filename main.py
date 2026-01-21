import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

import config
from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key is none")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model=config.model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        function_results = []

        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(
                    function_call, verbose=args.verbose
                )

                if not function_call_result.parts:
                    raise Exception("Error: function_call_result.parts is empty")

                first_part = function_call_result.parts[0]
                if first_part.function_response is None:
                    raise Exception("Error: .parts[0].function_response is None")

                if first_part.function_response.response is None:
                    raise Exception(
                        "Error: .parts[0].function_response.response is None"
                    )

                function_results.append(first_part)

                if args.verbose:
                    print(f"-> {first_part.function_response.response['result']}")

            messages.append(types.Content(role="user", parts=function_results))
            continue

        else:
            print(f"Final response:\n{response.text}")

            if args.verbose:
                user_token = response.usage_metadata.prompt_token_count
                response_token = response.usage_metadata.candidates_token_count
                print(f"User prompt: {messages}")
                print(f"Prompt tokens: {user_token}")
                print(f"Response tokens: {response_token}")
                return f"Response: \n{response.text}"
            else:
                return f"Response: \n{response.text}"

    print("Error: Maximum iterations reached without a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
