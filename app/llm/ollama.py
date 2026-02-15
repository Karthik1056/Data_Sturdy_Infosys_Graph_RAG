import ollama


def ask_ollama(prompt, model="qwen2.5:3b-instruct-q4_K_M"):

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']
