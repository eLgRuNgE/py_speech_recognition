from openai import OpenAI

client = OpenAI(api_key='aaaaaa')

def basic_test():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Summarize the following: OpenAI provides tools for developers to build applications with advanced AI models."}
            ]
        )
        print(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error during basic test: {e}")

basic_test()
