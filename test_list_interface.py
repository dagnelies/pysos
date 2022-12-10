import pysos
import unittest


class TestDictMethods(unittest.TestCase):
    def setUp(self):
        self.list = pysos.List("temp/list-interface.sos")
        self.list.clear()

    def tearDown(self):
        self.list.close()

    def test_empty_list_is_falsy(self):
        assert not self.list
        self.list.append("x")
        assert self.list
        self.list.clear()
        assert not self.list

    def test_append_elements(self):
        self.list.append(1)
        self.list.append("text")
        print(self.list[0])
        assert [1, "text"] == list(self.list)

    def test_delete_elements(self):
        self.list.extend([1, 2, 3, 4, 5])
        del self.list[1]
        del self.list[2]
        assert list(self.list) == [1, 3, 5]

    def test_change_elements(self):
        self.list.extend([1, 2, 3, 4, 5])
        self.list[1] = True
        self.list[2] = None
        self.list[3] = "value"
        assert list(self.list) == [1, True, None, "value", 5]

    def test_inserting_to_the_beginning(self):
        self.list.extend([2, 3])
        self.list.insert(0, 1)
        assert list(self.list) == [1, 2, 3]

    def test_inserting_elements_is_not_implemented(self):
        self.list.extend([1, 2])
        with self.assertRaises(NotImplementedError):
            self.list.insert(1, "value")

    def test_slicing(self):
        self.list.extend([1, 2, 3, 4, 5])
        assert [2, 3, 4] == list(self.list[1:-1])

    def test_remove_method(self):
        self.list.extend([1, "2", 3, 4])
        self.list.remove("2")
        assert [1, 3, 4] == list(self.list)

    def test_pop_method(self):
        self.list.extend([1, 2, 3, 4, 5])
        self.list.pop()
        assert [1, 2, 3, 4] == list(self.list)
        self.list.pop(1)
        assert [1, 3, 4] == list(self.list)

    def test_clear_method(self):
        self.list.extend([1, 2, 3])
        assert self.list
        self.list.clear()
        assert not self.list
    
    def test_contains(self):
        self.list.extend(["1", "2", "3"])
        assert "3" in self.list
        assert "5" not in self.list


if __name__ == "__main__":
    unittest.main()
