import openai

from settings import settings

prompt = """
Dear GPT-3.5 Turbo,

I'm designing a bot that will check for grammatical errors in chat conversations. I need your help in identifying these errors and reporting them back to me.

Please go through the following chat conversation and point out any grammatical errors you see. If there are no errors, please respond with 'Empty'.

Chat Conversation:
----------------------
""" # noqa


async def check_grammar(message):
    openai.api_key = settings.openai_token

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message},
        ],
    )
    final_response = response.choices[0]

    if final_response.message.content.lower() in ("empty", "empty."):
        return None

    return final_response
