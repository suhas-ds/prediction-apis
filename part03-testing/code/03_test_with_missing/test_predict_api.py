# test_predict_api.py
import json
import pytest
from pathlib import Path
from predict_api import app

# Find the directory where this script is.
# **ASSUMES THAT THE TEST DATASET FILES ARE HERE.
DATA_DIR = Path(__file__).parents[0]

@pytest.mark.parametrize('filename',
                         ['testdata_iris_v1.0.json',
                          'testdata_iris_missing_v1.0.json'])
def test_api_from_file(filename):
    dataset_fname = DATA_DIR.joinpath(filename)
    # Load all the test cases
    with open(dataset_fname) as f:
        test_data = json.load(f)

    with app.test_client() as client:
        for test_case in test_data:
            features = test_case['features']
            expected_response = test_case['expected_response']
            expected_status_code = test_case['expected_status_code']
            # Test client uses "query_string" instead of "params"
            response = client.get('/predict', query_string=features)
            # Check that we got expected status code back.
            assert response.status_code == expected_status_code
            # response.data returns a byte array, convert to a dict.
            assert json.loads(response.data) == expected_response
