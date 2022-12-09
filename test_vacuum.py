import pysos
import unittest
import pathlib


class TestVacuum(unittest.TestCase):
    def test_vacuum(self):
        reference_dict = {1: 2, "key": "value"}
        file_path = pathlib.Path("temp/vacuum.sos")
        my_dict = pysos.Dict(file_path)
        my_dict.clear()

        for i in range(999):
            my_dict["key"] = "x" * i
        my_dict.update(reference_dict)

        size_before_vacuum = file_path.stat().st_size
        my_dict.vacuum()
        size_after_vacuum = file_path.stat().st_size

        assert size_before_vacuum > size_after_vacuum
        assert my_dict == reference_dict
        my_dict.close()


if __name__ == "__main__":
    unittest.main()
