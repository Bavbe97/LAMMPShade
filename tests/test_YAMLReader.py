import unittest
import os
from unittest.mock import patch, MagicMock, mock_open
from lammpshade.YAMLReader import YAMLReader


class Test_YAMLReader_init_(unittest.TestCase):
    """
    Test the constructor of the YAMLReader class.
    """
    def test_init_file_not_found(self):
        """
        GIVEN: A non-existent filename
        WHEN: Instantiating the YAMLReader class with the non-existent filename
        THEN: It should raise a FileNotFoundError
        """

        with self.assertRaises(FileNotFoundError):
            # Instantiate the YAMLReader class with a non-existent filename
            YAMLReader("non_existent_file.yaml")


class Test_YAMLReader_convert_value(unittest.TestCase):
    """
    Tests the convert_value method of the YAMLReader class.
    """
    def test_convert_value_int(self):
        """
        GIVEN: An integer string
        WHEN: Calling the convert_value method with the integer string
        THEN: It should return the corresponding integer value
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with an integer string
        assert yaml_reader.convert_value("123") == 123
        assert yaml_reader.convert_value("-123") == -123

    def test_convert_value_float(self):
        """
        GIVEN: A float string
        WHEN: Calling the convert_value method with the float string
        THEN: It should return the corresponding float value
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with a float string
        assert yaml_reader.convert_value("3.14") == 3.14
        assert yaml_reader.convert_value("-3.14") == -3.14
        assert yaml_reader.convert_value("3.14e-2") == 3.14e-2
        assert yaml_reader.convert_value("-3.14e-2") == -3.14e-2
        assert yaml_reader.convert_value("3.14e2") == 3.14e2

    def test_convert_value_list_integers(self):
        """
        GIVEN: A list of integer strings
        WHEN: Calling the convert_value method with the list of integer strings
        THEN: It should return a list of corresponding integer values
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with a list of integer strings
        assert yaml_reader.convert_value("[1, 2, 3]") == [1, 2, 3]

    def test_convert_value_list_strings(self):
        """
        GIVEN: A list of string strings
        WHEN: Calling the convert_value method with the list of string strings
        THEN: It should return a list of corresponding string values
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with a list of string strings
        assert yaml_reader.convert_value("[hello, world.]") == ['hello',
                                                                'world.']

    def test_convert_value_list_mixed(self):
        """
        GIVEN: A list of mixed type strings
        WHEN: Calling the convert_value method with the list of mixed type
              strings
        THEN: It should return a list of corresponding mixed type values
        """

        yaml_reader = YAMLReader(os.path.join('tests', 'test.yaml'))
        # Call the convert_value method with a list of mixed type strings
        assert yaml_reader.convert_value("[1, 2.5, hello]") == [1, 2.5,
                                                                'hello']


class Test_YAMLReader_get_next_step(unittest.TestCase):
    """
    Tests the get_next_step method of the YAMLReader class.
    """
    def test_get_next_step_subsequent_key_value_pairs(self):
        """
        GIVEN: A YAML file with subsequent key-value pairs
        WHEN: Calling the get_next_step method
        THEN: It should return the subsequent key-value pairs from the YAML
              file
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        natoms: 10
        units: real
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader("test_filename.yaml")
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['natoms'] == 10
            assert step['units'] == 'real'
            # Verify that the close method of the mock file object is called
            # exactly once
            mock_file.close.assert_called_once()

    def test_get_next_step_key_value_then_key_dictionaries(self):
        """
        GIVEN: A YAML file with subsequent key-value pairs and then a
               key-dictionary pair
        WHEN: Calling the get_next_step method
        THEN: It should return the subsequent key-value pairs and then the
              key-dictionary pair from the YAML file
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        natoms: 10
        thermo:
        - keywords: [ Step, Time, Quantity, ]
        - data: [ 0, 0, 300.01337588855796, ]
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader("test_filename.yaml")
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['natoms'] == 10
            assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity']
            assert step['thermo']['data'] == [0, 0, 300.01337588855796]
            # Verify that the close method of the mock file object is called
            # exactly once
            mock_file.close.assert_called_once()

    def test_get_next_step_key_value_then_key_lists(self):
        """
        GIVEN: A YAML file with subsequent key-value pairs and then a key-list
               pair
        WHEN: Calling the get_next_step method
        THEN: It should return the subsequent key-value pairs and then the
              key-list pair from the YAML file
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        natoms: 10
        box:
        - [ 0, 53 ]
        - [ 0, 52.57 ]
        - [ 0.439, 96.33 ]
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader('test_filename.yaml')
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['natoms'] == 10
            assert step['box'] == [[0, 53],
                                   [0, 52.57],
                                   [0.439, 96.33]]

    def test_get_next_step_key_dictionaries_then_key_lists(self):
        """
        GIVEN: A YAML file with subsequent key-dictionary pairs and then a
               key-list pair
        WHEN: Calling the get_next_step method
        THEN: It should return the subsequent key-dictionary pairs and then
              the key-list pair from the YAML file
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        thermo:
        - keywords: [ Step, Time, Quantity, ]
        - data: [ 0, 0, 300.01337588855796, ]
        box:
        - [ 0, 53 ]
        - [ 0, 52.57 ]
        - [ 0.439, 96.33 ]
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader('test_filename.yaml')
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity']
            assert step['thermo']['data'] == [0, 0, 300.01337588855796]
            assert step['box'] == [[0, 53],
                                   [0, 52.57],
                                   [0.439, 96.33]]

    def test_get_next_step_file_ends(self):
        """
        GIVEN: A YAML file that ends
        WHEN: Calling the get_next_step method
        THEN: It should return an empty dictionary
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader("test_filename.yaml")
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step == {}
            step = yaml_reader.get_next_step()

            # Verify that the close method of the mock file object is called
            # exactly once
            mock_file.close.assert_called_once()

    def test_get_next_step_key_lists_then_key_dictionaries(self):
        """
        GIVEN: A YAML file with subsequent key-list pairs and then a
               key-dictionary pair
        WHEN: Calling the get_next_step method
        THEN: It should return the subsequent key-list pairs and then the
              key-dictionary pair from the YAML file
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        box:
        - [ 0, 53 ]
        - [ 0, 52.57 ]
        - [ 0.439, 96.33 ]
        thermo:
            - keywords: [ Step, Time, Quantity, ]
            - data: [ 0, 0, 300.01337588855796, ]
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader('test_filename.yaml')
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['box'] == [[0, 53],
                                   [0, 52.57],
                                   [0.439, 96.33]]
            assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity']
            assert step['thermo']['data'] == [0, 0, 300.01337588855796]

    def test_get_next_step_key_dictionaries_then_key_value(self):
        """
        Test that the get_next_step method returns subsequent key-dictionary
        pairs and then a key-value pair from the YAML file.

        GIVEN: A YAML file with subsequent key-dictionary pairs and then a
               key-value pair
        WHEN: Calling the get_next_step method
        THEN: It should return the subsequent key-dictionary pairs and then
              the key-value pair from the YAML file
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        thermo:
        - keywords: [ Step, Time, Quantity, Negative, Exponential, ]
        - data: [ 0, 0, 300.01337588855796, -26, -6.5e-3, ]
        natoms: 10
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader("test_filename.yaml")
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['thermo']['keywords'] == ['Step', 'Time', 'Quantity',
                                                  'Negative', 'Exponential']
            assert step['thermo']['data'] == [0, 0, 300.01337588855796, -26,
                                              -6.5e-3]
            assert step['natoms'] == 10
            # Verify that the close method of the mock file object is called
            # exactly once
            mock_file.close.assert_called_once()

    def test_get_next_step_key_lists_then_key_value(self):
        """
        Test that the get_next_step method returns subsequent key-list pairs
        and then a key-value pair from the YAML file.

        GIVEN: A YAML file with subsequent key-list pairs and then a key-value
               pair
        WHEN: Calling the get_next_step method
        THEN: It should return the subsequent key-list pairs and then the
              key-value pair from the YAML file
        """

        # Define YAML content to simulate reading from a file
        yaml_content = '''---
        box:
        - [ 0, 53 ]
        - [ 0, 52.57 ]
        - [ 0.439, 96.33 ]
        natoms: 10
        ...'''
        # Create a mock file object
        mock_file = MagicMock()
        # Configure the readline method of the mock file to return lines of
        # YAML content
        mock_file.readline.side_effect = yaml_content.splitlines(True) + ['']

        # Patch the open function to return the mock file object
        with patch('builtins.open', return_value=mock_file):
            yaml_reader = YAMLReader('test_filename.yaml')
            # Call the get_next_step method
            step = yaml_reader.get_next_step()
            # Assert the expected behaviour
            assert step['box'] == [[0, 53],
                                   [0, 52.57],
                                   [0.439, 96.33]]
            assert step['natoms'] == 10

    def test_get_next_step_get_subsequent_step(self):
        """
        GIVEN: A YAML file with subsequent steps
        WHEN: Calling the get_next_step method multiple times
        THEN: It should return the subsequent steps from the YAML file
        """

        # Define YAML lines to simulate reading from a file
        yaml_lines = [
            "---",
            "natoms: 10",
            "...",
            "---",
            "creator: LAMMPS",
            "box:",
            "  - [ 0, 53 ]",
            "  - [ 0, 52.57 ]",
            "  - [ 0.439, 96.33 ]",
            "..."
        ]

        # Create a mock file object
        mock_file = mock_open(read_data='\n'.join(yaml_lines))

        # Patch the open function to return the mock file object
        with patch('builtins.open', mock_file):
            # Instantiate the YAMLReader class with a fake filename
            yaml_reader = YAMLReader("fake_filename.yaml")

            # Call the get_next_step method until '...' is encountered
            step = yaml_reader.get_next_step()
            step = yaml_reader.get_next_step()

            # Assert the expected behavior
            assert 'natoms' not in step
            assert step['creator'] == 'LAMMPS'
            assert step['box'] == [[0, 53], [0, 52.57], [0.439, 96.33]]


if __name__ == '__main__':
    unittest.main()
