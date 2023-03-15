import os

import openai
import azure.cognitiveservices.speech as speechsdk

import winsound

import easygui

import pyperclip

class Chatbot():
    def __init__(self, *args,):
        #CLES API
        self._openai_key = "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"
        self._azure_speech_key = "b736e203fe004d99b5d92d2f2e68c5da"
        self._region = "francecentral"
        #MODE D'ECHANGE
        self.visual_mode = False
        self._has_ended = False
        #SON DE MICRO ON/OFF
        self._mic_on_sound = "D:\George\Documents\Envs\mychat\\notif.wav"
        #OBJET CONFIG DE LA RECO VOCALE
        self._reco_config = speechsdk.SpeechConfig(
            subscription = self._azure_speech_key, 
            region = self._region)
        #LANGUE DE LA RECO VOCALE
        self._reco_config.speech_recognition_language = "fr-FR"
        #OBJET CONFIG AUDIO DE LA RECO VOCALE
        self._audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        #OBJET RECO VOCALE FINAL
        self._speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config = self._reco_config, 
            audio_config = self._audio_config)
        #SYNTHESE VOCALE
        self._speech_config = speechsdk.SpeechConfig(subscription=self._azure_speech_key, region=self._region)
        self._speech_config.speech_synthesis_voice_name = "fr-CA-SylvieNeural"
        self._speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self._speech_config)
        #ELEMENTS DE CONTEXTE DE LA DISCUSSION
        self._system_prompt_loc = os.path.join("D:\George\Documents\Envs\mychat\prompting")
        if os.path.exists(os.path.join(self._system_prompt_loc, "sysprompt.txt")):
            with open(os.path.join(self._system_prompt_loc, "sysprompt.txt"), 'r') as f:
                self._system_prompt = f.read()
        else:
            self._system_prompt = ""
        #LE TABLEAU QUI CONTIENDRA LES MESSAGES DE LA DISCUSSION    
        self._messages = []

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

    def set_visual(self, visual_mode:bool = True)->None:
        if type(visual_mode) == bool: self.visual_mode = visual_mode

    def add_user_prompt(self, prompt:str)->None:
        self._messages.append({"role": "user", "content": prompt})

    def add_assistant_answer(self, answer:str)->None:
        self._messages.append({"role": "assistant", "content": answer})

    def register_message_box(self,frame):
        self._message_box = frame

    #FONCTIONS HELPER
    def edit_system_prompt(self) -> None:
        self._set_system_promp(
            easygui.textbox(
                msg = "Veuillez rentrer le prompt système initial.",
                title = "System Prompt",
                text=self._system_prompt
            ))
        with open(os.path.join(self._system_prompt_loc, "sysprompt.txt"), "w") as f:
            f.write(self._system_prompt)

    def check_words(self,prompt:str, words:str, consecutif:bool=True)->bool:
        prompt = prompt.lower()
        prompt = prompt.replace(".", "")
        prompt = prompt.replace("?", "")
        words = [word.lower() for word in words]
        indices = [i for i, word in enumerate(prompt.split()) if word in words]
        if consecutif:
            for i in range(len(indices) - 1):
                if indices[i] + 1 != indices[i+1]:
                    return False
            return True
        else:
            return len(indices) == len(words)

    #FONCTIONS DE DISCUSSION
    def get_prompt(self)->str:
        prompt = None
        while(
        prompt == None or
        prompt == "Visuel." or
        prompt == "Audio." or
        prompt == "Copier." or
        prompt == "Afficher."):
            #TRAITEMENT DU MODE VISUEL OU NON
            if not self.visual_mode:
                prompt = self.get_microphone()
            else:
                prompt = easygui.textbox(
                    title="Veuillez rentrer votre réponse.", 
                    msg="Votre réponse :")
                if prompt[-1] != ".":
                    prompt = prompt + "."
                prompt = prompt.capitalize()
            #TRAITEMENT DES COMMANDES DE CONTROLE
            #FONCTIONS D'INTERCEPTION DU PROMPT
            if prompt == "Visuel." and not self.visual_mode:
                self.set_visual()(True)
                print("Passage en mode visuel.")
            elif prompt == "Audio." and self.visual_mode:
                self.set_visual()(False)
                self.read_speech("Passage en mode vocal.")
            elif prompt == "Copier." and not self.visual_mode:
                self.read_speech("Réponse copiée dans le presse-papier.")
                pyperclip.copy(self.assistant_messages[-1])
            elif prompt == "Afficher." and not self.visual_mode:
                easygui.textbox(
                    title="Réponse",
                    text = self.assistant_messages[-1])
        #TRAITEMENT DE LA FIN DU DIALOGUE
        #FONCTIONS DE POST-TRAITEMENT DU PROMPT
        if prompt == "Stop.":
            self._has_ended = True
            prompt = "Je mets fin à notre discussion."
        elif self.check_words(prompt, ["presse-papier"], False):
            prompt = prompt + "\nContenu du presse-papier:\n" + pyperclip.paste()
        return prompt

    def converse(self):
        #EDITION DU SYS PROMPT
        self.edit_system_prompt()
        #AJOUT DANS LA PILE DE CONVERSATION
        self._messages.append({"role": "system", "content" : self._system_prompt})
        while not self._has_ended:
            prompt = self.get_prompt()
            self.add_user_prompt(prompt)(prompt=prompt)
            completion_package = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self._messages,
                api_key=self._openai_key)
            response = completion_package.choices[0].message.content
            self.add_assistant_answer(answer)(response)
            if self.visual_mode:
                easygui.textbox(
                    title = "Réponse",
                    text=response)
            else:
                self.read_speech(response)

    #FONCTIONS COGNITIVES
    def get_microphone(self)->str:
        """Une fois cette fonction lancée, elle écoute au micro par défaut, arrête son écoute une fois que l'utilisateur arrête de parler, puis renvoie sous la forme d'un string ce qu'elle a entendu.

        Returns:
            str: Le contenu reconnu par la fonction
        """        
        winsound.PlaySound(
            self._mic_on_sound, 
            winsound.SND_ASYNC | winsound.SND_ALIAS )
        print("Speak into your microphone.")
        speech_recognition_result = self._speech_recognizer.recognize_once_async().get()
        winsound.PlaySound(
            self._mic_on_sound, 
            winsound.SND_ASYNC | winsound.SND_ALIAS )
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return speech_recognition_result.text
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            return None
             
    def read_speech(self, text:str)->None:
        """J'ai vraiment besoin d'expliquer ?
        Args:
            text (str): Le texte que la fonction lira en mode vocal.
        """        
        self._speech_synthesizer.speak_text_async(text).get()



if __name__ == "__main__":
    new_chat = Chatbot()
    new_chat.converse()