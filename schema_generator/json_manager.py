import json
import os
from typing import Tuple, List, Dict, Union


JSONObject = Union[int, float, bool, str, List, Dict, None]


class JSONObjectsManager:
    """
    Class to read multiple json files and manage resulting objects.
    
    :param: folder_path: str: folder that contains json files.
    :param: dump_path: str: optional: default folder to dump json files in 
        when .dump_all_json method is called.

    Provides all_json property that returns list of json objects from files.
    Provides dump_all_json method to dump json objects into files.
    """

    def __init__(
            self, folder_path: str, dump_path: str = "") -> None:
        
        self._folder_path = folder_path
        self._dump_path = dump_path
        
    @property
    def all_json(self):
        return [json_item[0] for json_item in self.all_json_plus_filename]
    
    @property
    def all_json_plus_filename(self):
        return self._load_all_json()
        
    def dump_all_json(self, 
                json_objs: List[Tuple[JSONObject, str]], dump_path: str = ""):
        """
        Write list of JSONObject objects to files.

        dump_path defaults to dump_path passed during object 
        instantiation if not provided.
        """
        assert dump_path or self._dump_path, \
            "dump_path must be provided if not specified during instantiation"
        
        dump_path = dump_path if dump_path else self._dump_path

        for json_plus_filename in json_objs:
            self.dump_json_to_file(
                json_plus_filename[0], 
                self._get_dump_path(json_plus_filename[1], dump_path)
            )

    @staticmethod
    def dump_json_to_file(
            data: JSONObject, file_path: str) -> JSONObject:
        """
        Write specific JSONObject object to file.
        """ 
        with open(os.path.abspath(file_path), "w") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def load_json_file(file_path) -> JSONObject:
        """
        Read json file into JSONObject.
        """
        with open(file_path, "r") as file:
            return json.load(file)

    def _get_dump_path(self, filename: str, dump_path: str) -> str:
        """
        Get path of file to dump json data into.
        """
        dump_filename = f"{filename.split('.')[:-1][0]}_schema.json"
        dump_path = os.path.join(dump_path, dump_filename)
        return dump_path

    def _load_all_json(self) -> List[Tuple[JSONObject, str]]:
        """
        Read all json files in folder into list of two-tuples of JSONObject 
        and the origin file's name.
        """
        self._files = [file for file in os.listdir(self._folder_path) 
                 if file.split(".")[-1].lower()=="json"]
        
        all_json_plus_filename = [
            (self.load_json_file(os.path.join(self._folder_path, file_name)),
                file_name) 
            for file_name in self._files
        ]
        return all_json_plus_filename
            
