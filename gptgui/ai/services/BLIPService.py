import replicate
import deepl
import os


class BLIPService():
    def __init__(self, outcome:dict, img_path:str, query:str|None=None) -> None:
        self._translator = deepl.Translator(
            auth_key=os.environ.get("DEEPL_API_TOKEN")) # type: ignore
        self._outcome = outcome
        self._img_path = img_path
        self._query = query

    def get_package(self,):
        if self._query == None:
            output = replicate.run(
                        "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
                        input={"image": open(self._img_path, "rb")})
        else:
            output = replicate.run(
                        "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
                        input={"image": open(self._img_path, "rb"),
                               "task":"visual_question_answering",
                               "question":str(self._translator.translate_text(
                                    self._query, 
                                    target_lang="EN-GB"))})
        print(output)
        output = str(self._translator.translate_text(
            output,
            target_lang="FR"))
        return str(output)
    
    