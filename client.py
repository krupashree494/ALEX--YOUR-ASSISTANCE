import google.generativeai as genai

# Set up API key
genai.configure(api_key="AIzaSyB7g07gML59K_QbJI7L76GAVwMCy5jGT1A")  # Replace with your key

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Use available model
    response = model.generate_content(prompt)
    return response.text

# Example usage
if __name__ == "__main__":
    prompt = "What is coding?"
    answer = chat_with_gemini(prompt)
    print("Gemini's Response:", answer)
