from schema_generator.json_manager import JSONObjectsManager, JSONObject
from schema_generator.schema_reader import SchemaReader

from typing import List, Tuple
import logging


folder_path = "./data"
json_objects_manager = JSONObjectsManager(folder_path)

logger = logging.getLogger()


def load_all_json(
        json_manager: JSONObjectsManager = json_objects_manager
    ) -> List[Tuple[JSONObject, str]]:
    """
    Read all json files in folder into list of two-tuples of JSONObject 
    and the origin file's name.
    """
    all_json_plus_filename = json_manager.all_json_plus_filename
    return all_json_plus_filename


def read_json_schema(obj: JSONObject) -> JSONObject:
    """
    Return schema of obj.
    """
    schema_reader = SchemaReader(obj)
    schema = schema_reader.schema
    return schema


def read_all_json_schemas(
        all_json: List[Tuple[JSONObject, str]]) -> \
            List[Tuple[JSONObject, str]]:
    """
    Return a list of two-tuples of schemas of json files 
    and the origin file's name.
    """
    all_json_schemas = [(read_json_schema(json_object[0]), json_object[1])
                        for json_object in all_json]
    return all_json_schemas


def dump_all_json(json_objs: List[Tuple[JSONObject, str]]) -> None:
    """
    Write list of JSONObject objects to files.
    """
    json_objects_manager.dump_all_json(json_objs)


def main():
    print("Loading json files...")
    all_json_plus_filename = load_all_json()

    print("Reading schemas...")
    all_json_schemas = read_all_json_schemas(all_json_plus_filename)

    print("Writing schemas to ./schema/...")
    dump_all_json(all_json_schemas)


if __name__=="__main__":
    main()