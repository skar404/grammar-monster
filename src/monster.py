from typing import Optional

import openai

from settings import settings

prompt = """
Go through the following chat conversation and point out any grammatical errors you see. If there are no errors, please respond with 'Empty'

Message: ```{message}```
"""  # noqa


async def check_grammar(message: str) -> Optional[str]:
    openai.api_key = settings.openai_token

    response = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=prompt.format(message=message),
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    final_response = response.choices[0].text
    if final_response.lower().strip() == 'empty':
        return None

    return final_response


if __name__ == '__main__':
    # debug code
    import asyncio

    data = asyncio.run(check_grammar("""emptys"""))
    print(data)
