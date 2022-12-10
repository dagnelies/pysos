import pysos
import unittest


class TestDictMethods(unittest.TestCase):
    def setUp(self):
        self.db = pysos.Dict("temp/dict-interface.sos")
        self.db.clear()

    def tearDown(self):
        self.db.close()

    def test_list_of_keys(self):
        self.db["key1"] = "value1"
        self.db["key2"] = "value2"
        assert set(list(self.db)) == {"key1", "key2"}
        assert set(self.db.keys()) == {"key1", "key2"}

    def test_length_is_the_number_of_elements(self):
        assert len(self.db) == 0
        self.db["key1"] = "value1"
        assert len(self.db) == 1
        self.db["key2"] = "value2"
        assert len(self.db) == 2
        self.db.clear()
        assert len(self.db) == 0

    def test_values_can_be_set_and_get(self):
        self.db["key"] = "value"
        assert self.db["key"] == "value"
        with self.assertRaises(KeyError):
            self.db["missing"]

    def test_delete_element_from_dict(self):
        self.db["key"] = "value"
        del self.db["key"]
        with self.assertRaises(KeyError):
            self.db["key"]

    def test_in_operator(self):
        self.db["key"] = "value"
        assert "key" in self.db
        assert "missing" not in self.db

    def test_iter_function(self):
        self.db["key1"] = "value1"
        self.db["key2"] = "value2"
        assert {"key1", "key2"} == set(iter(self.db))

    def test_empty_dict_is_falsy(self):
        assert not self.db
        self.db["key"] = "value"
        assert self.db

    def test_clear_method(self):
        self.db["key"] = "value"
        assert self.db
        self.db.clear()
        assert not self.db

    def test_get_method(self):
        self.db["key"] = "value"
        assert self.db.get("key", "missing") == "value"
        assert self.db.get("key2", "missing") == "missing"

    def test_items_method(self):
        self.db["key1"] = "value1"
        self.db["key2"] = "value2"
        other_dict = {}
        for key, value in self.db.items():
            other_dict[key] = value
        assert other_dict == self.db

    def test_pop_method(self):
        self.db["key"] = "value"
        assert self.db.pop("key") == "value"
        assert "key" not in self.db
        assert self.db.pop("key", "default") == "default"
        with self.assertRaises(KeyError):
            self.db.pop("key")

    def test_setdefault_method(self):
        self.db.setdefault("key", "default")
        assert self.db["key"] == "default"
        self.db["key2"] = "value"
        self.db.setdefault("key2", "default")
        assert self.db["key2"] == "value"

    def test_update_method(self):
        reference_dict = {"key1": "value1", "key2": "value2"}
        self.db.update(reference_dict)
        assert self.db == reference_dict

    def test_values_method(self):
        self.db["key1"] = "value1"
        self.db["key2"] = "value2"
        assert set(self.db.values()) == {"value1", "value2"}


if __name__ == "__main__":
    unittest.main()
