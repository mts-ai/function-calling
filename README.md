# Function Calling in AI Applications

**Function calling** allows you to integrate Large Language Models (LLMs) with external tools for effective usage and interaction with APIs.

LLMs like GPT-4 and GPT-3.5 can detect when a function needs to be called and generate JSON arguments for those functions. These functions act as tools in your AI application, and multiple functions can be defined in a single request.

## Basic Sequence of Steps for Function Calling

1. **Initial Call:** Call the model with the user query and a set of functions defined in the functions parameter.
   
2. **Function Detection:** The model can choose to call one or more functions. The content will be a stringified JSON object in your custom schema (note: the model may hallucinate parameters).

3. **Parsing and Execution:** Parse the string into JSON in your code, and call your function with the provided arguments if they exist.
   
4. **Response Handling:** Call the model again, appending the function response as a new message. Let the model summarize the results back to the user.

## Example: Sending Email with Gemini and Open Source Models

```python
def multiply(a:float, b:float):
    """returns a * b."""
    return a*b



def send_email(destination_email: str, message_text: str):
    """Send message to user_email with message_text"""

    email = ''
    password = ''
    dest_email = destination_email
    subject = 'Test'
    email_text = message_text

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                        dest_email, 
                                                        subject, 
                                                        email_text)

    server = smtp.SMTP_SSL('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(email, password)
    server.auth_plain()
    server.sendmail(email, dest_email, message)
    server.quit()

model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              tools=[multiply, send_email])

chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message('Send a message to email about meeting on June 13. And tell him to call my number back. Be kind')
response.text
```

## Contributing

We welcome contributions from the community. Please read our contributing guidelines and code of conduct.

## License

function-calling is licensed under the MIT License. See the LICENSE file for more information.

## Contact

For any questions, issues, or suggestions, please open an issue on our [GitHub repository](https://github.com/mts-ai/function-calling).