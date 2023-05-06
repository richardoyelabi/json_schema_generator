import unittest
from ...schema_generator.schema_reader import SchemaReader


class TestGetListItemTypes(unittest.TestCase):
    """
    Test SchemaReader._get_list_item_types.
    """
    def setUp(self) -> None:
        json_object = dict()
        self.schema_reader = SchemaReader(json_object)

    def run_test(self):
        obj = [3, 5,"test string\n", 3.2, False, [2,3,"four"], 0.34, {"key": 74123, "nan": "value"}]
        types = self.schema_reader._get_list_item_types(obj)
        self.assertEqual(types, [int, str, float, bool, list, dict])


if __name__ == '__main__':
    unittest.main()