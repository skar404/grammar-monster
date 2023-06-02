from typing import Optional

import openai

from settings import settings

prompt = """Check English grammatical in the chat and write about mistake with detail, you need say "Empty" if you don't see any mistakes.
Chat message: {message}
"""  # noqa


async def check_grammar(message: str) -> Optional[str]:
    openai.api_key = settings.openai_token

    response = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=prompt.format(message=message),
        temperature=0,
        max_tokens=len(prompt.format(message=message)),
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    final_response = response.choices[0].text
    if final_response.lower().strip().replace('.', '') == 'empty':
        return None

    return final_response


if __name__ == '__main__':
    # debug code
    import asyncio

    data = asyncio.run(check_grammar("""emptys"""))
    print(data)
