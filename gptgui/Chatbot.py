import os
import openai
import tiktoken

class Chatbot():
    def __init__(self, *args,):
        #CLES API
        self._openai_key = "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"
        self._azure_speech_key = "b736e203fe004d99b5d92d2f2e68c5da"
        self._region = "francecentral"
        self._has_ended = False
        #ELEMENTS DE CONTEXTE DE LA DISCUSSION
        self._system_prompt_loc = os.path.join("D:\\George\\Documents\\Envs\\mychat\\prompting")
        if os.path.exists(os.path.join(self._system_prompt_loc, "sysprompt.txt")):
            with open(os.path.join(self._system_prompt_loc, "sysprompt.txt"), 'r') as f:
                self._system_prompt = f.read()
        else:
            self._system_prompt = ""
        #LE TABLEAU QUI CONTIENDRA LES MESSAGES DE LA DISCUSSION    
        self._messages = []
        self._messages.append({"role": "system", "content" : self._system_prompt})

        #FENETRE
        self._message_box = None

    #FONCTIONS ATTRIBUS
    @property
    def user_messages(self):
        return [x["content"] for x in self._messages if x["role"] == "user"]

    @property
    def assistant_messages(self):
        return [x["content"] for x in self._messages if x["role"] == "assistant"]

    @property
    def all_messages(self):
        return [x["content"] for x in self._messages if x["role"] != "system"]

    #FONCTIONS GETSETADD
    def set_system_prompt(self, prompt:str)->None:
        self._system_prompt = prompt

    def add_user_prompt(self, prompt:str)->None:
        self._messages.append({"role": "user", "content": prompt})

    def add_assistant_answer(self, answer:str)->None:
        self._messages.append({"role": "assistant", "content": answer})
    #FONCTIONS HELPER

    def __str__(self) -> str:
        return "\n".join([str(x["role"])+":"+str(x["content"]) for x in self._messages[1:]])

    #FONCTION THREADEE QUI AGIT SUR 
    def return_answer(self)->str:
        completion_package = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self._messages,
                api_key=self._openai_key)
        response = completion_package.choices[0].message.content # type: ignore
        return response
    
    def num_tokens_from_messages(self):
        """Returns the number of tokens used by a list of messages."""
        model = "gpt-3.5-turbo-0301"
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
            num_tokens = 0
            for message in self._messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")