import replicate

class BLIPService():
    def __init__(self, outcome:dict, img_path:str) -> None:
        self._outcome = outcome
        self._img_path = img_path

    def get_package(self,):
        output = replicate.run(
                    "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
                    input={"image": open(self._img_path, "rb")})
        print(output)
        return str(output)
    
    