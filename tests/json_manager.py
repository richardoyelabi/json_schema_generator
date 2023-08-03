from unittest import TestCase, mock
from schema_generator.json_manager import JSONObjectsManager

import os


@mock.patch.object(JSONObjectsManager, "dump_json_to_file")
@mock.patch.object(JSONObjectsManager, "load_json_file")
class JSONObjectsManagerTest(TestCase):
    def setUp(self) -> None:
        self.folder_path = "folder_path/"
        self.dump_path = "dump_path/"

        self.json_file_names = ["json_file_name_1.json", "json_file_name_2.JSON"]
        self.json_file_paths = [
            self.folder_path + file_name for file_name in self.json_file_names
        ]
        self.all_json_objects = [
            mock.MagicMock(name="json_file_object_1"),
            mock.MagicMock(name="json_file_object_2"),
        ]
        self.other_file_names = ["other_file_name_1.txt", "other_file_name_2.png"]

        self.all_file_names = self.json_file_names + self.other_file_names

        self.all_json_plus_filename = list(
            zip(self.all_json_objects, self.json_file_paths)
        )

        self.manager = JSONObjectsManager(self.folder_path, self.dump_path)

    def test_init(self, load_json_file, dump_json_to_file):
        self.assertEqual(self.manager._folder_path, self.folder_path)
        self.assertEqual(self.manager._dump_path, self.dump_path)

    @mock.patch("os.listdir")
    def test__load_all_json(self, listdir, load_json_file, dump_json_to_file):
        os.listdir.return_value = self.all_file_names

        all_json_plus_file_name = self.manager._load_all_json()
        self.assertEqual(self.manager._files, self.json_file_names)
        load_json_file.assert_has_calls(
            [mock.call(file_path) for file_path in self.json_file_paths]
        )
        expected_all_json_plus_file_name = [
            (load_json_file.return_value, file_name)
            for file_name in self.json_file_names
        ]
        self.assertEqual(all_json_plus_file_name, expected_all_json_plus_file_name)

    @mock.patch.object(JSONObjectsManager, "_load_all_json")
    def test_all_json_plus_filename(
        self, _load_all_json, load_json_file, dump_json_to_file
    ):
        _load_all_json.return_value = self.all_json_plus_filename
        self.assertEqual(
            self.manager.all_json_plus_filename, self.all_json_plus_filename
        )

    @mock.patch.object(JSONObjectsManager, "_load_all_json")
    def test_all_json(self, _load_all_json, load_json_file, dump_json_to_file):
        _load_all_json.return_value = self.all_json_plus_filename
        self.assertAlmostEqual(self.manager.all_json, self.all_json_objects)

    def test__get_dump_path(self, load_json_file, dump_json_to_file):
        test_file_name = "test_file_name.json"
        dump_path = self.manager._get_dump_path(test_file_name, self.dump_path)
        self.assertEqual(dump_path, self.dump_path + "test_file_name_schema.json")

    @mock.patch.object(JSONObjectsManager, "_get_dump_path")
    def test_dump_all_json(self, _get_dump_path, load_json_file, dump_json_to_file):
        manager_without_dump_path = JSONObjectsManager("no_dump_path_folder_path")

        for manager in (manager_without_dump_path, self.manager):
            with self.subTest(
                msg="JSONManager instantiated without dump_path specified"
            ):
                if manager == manager_without_dump_path:
                    self.assertRaises(
                        AssertionError,
                        manager.dump_all_json,
                        self.all_json_plus_filename,
                    )

                manager.dump_all_json(self.all_json_plus_filename, self.dump_path)
                manager._get_dump_path.assert_has_calls(
                    [
                        mock.call(file_path, self.dump_path)
                        for file_path in self.json_file_paths
                    ]
                )
                manager.dump_json_to_file.assert_has_calls(
                    [
                        mock.call(file_obj, manager._get_dump_path.return_value)
                        for file_obj in self.all_json_objects
                    ]
                )
