import json
import smtplib as smtp
from getpass import getpass
import re
import ast
from transformers import AutoTokenizer, AutoModelForCausalLM

class FuncCallModel:
    def __init__(self):
        super().__init__()

        self.tokenizer = AutoTokenizer.from_pretrained("gorilla-llm/gorilla-openfunctions-v2")
        self.model = AutoModelForCausalLM.from_pretrained("gorilla-llm/gorilla-openfunctions-v2")

        self.functions = [
                {
                    "name": "send_email",
                    "description": "Send message to user_email with message_text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "destination_email": {
                                "type": "string",
                                "description": "Destination email",
                            },
                            "message_text": {
                                "type": "string",
                                "description": "Text of message",
                            },
                        },
                        "required": ["destination_email", "message_text"],
                    },
                }
            ]


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


    def get_prompt(user_query: str, functions: list = []) -> str:
        """
        Generates a conversation prompt based on the user's query and a list of functions.

        Parameters:
        - user_query (str): The user's query.
        - functions (list): A list of functions to include in the prompt.

        Returns:
        - str: The formatted conversation prompt.
        """
        system = "You are an AI programming assistant, utilizing the Gorilla LLM model, developed by Gorilla LLM, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer."
        if len(functions) == 0:
            return f"{system}\n### Instruction: <<question>> {user_query}\n### Response: "
        functions_string = json.dumps(functions)
        return f"{system}\n### Instruction: <<function>>{functions_string}\n<<question>>{user_query}\n### Response: "
    

    def generate(self, prompt):
        formatted_prompt = self.get_prompt(prompt, functions=self.functions)
        tokenized_prompt = self.tokenizer(formatted_prompt, return_tensors='pt')
        res = self.model.generate(**tokenized_prompt, max_length=500)

        responce = self.tokenizer.decode(res[0], skip_special_tokens=True)
        func_call = responce.split("<<function>>")[-1]
        func_name = func_call.split("(")[0]
        str_args = "{" + func_call.split("(")[1].replace("=", ":").replace(")", "}")
        input_str = str_args
        pattern = r"(\w+):"
        output_str = re.sub(pattern, r'"\1":', input_str)
        args = ast.literal_eval(output_str)   

        try: 
            locals()[func_name](**args)
            print("FUNCTION EXECUTED")
        except:
            return responce