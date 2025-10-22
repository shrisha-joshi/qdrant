import pytest

from .helpers.collection_setup import basic_collection_setup, drop_collection
from .helpers.helpers import request_with_validation


@pytest.fixture(autouse=True, scope="module")
def setup(on_disk_vectors, collection_name):
    basic_collection_setup(collection_name=collection_name, on_disk_vectors=on_disk_vectors)
    yield
    drop_collection(collection_name=collection_name)


def test_validations(collection_name):
    response = request_with_validation(
        api="/collections/{collection_name}/points/query",
        method="POST",
        path_params={"collection_name": collection_name},
        body={
            "query": {
                "feedback": {
                    "target": [0.1, 0.2, 0.3, 0.4],
                    "feedback": [ {"vector": 10000, "score": 0.85} ],
                    "strategy": {
                        "naive": {
                            "a": 0.12,
                            "b": 1.25,
                            "c": 0.99
                        }
                    }
                }
            }
        },
    )
    assert not response.ok, response.text
    assert response.json()["status"]["error"] == "Not found: No point with id 10000 found"

    response = request_with_validation(
        api="/collections/{collection_name}/points/query",
        method="POST",
        path_params={"collection_name": collection_name},
        body={
            "query": {
                "feedback": {
                    "target": [0.1, 0.2, 0.3, 0.4],
                    "feedback": [  ],
                    "strategy": {
                        "naive": {
                            "a": 0.12,
                            "b": 1.25,
                            "c": 0.99
                        }
                    }
                }
            }
        },
    )
    assert not response.ok, response.text
    assert "feedback elements must be non-empty" in response.json()["status"]["error"]

    response = request_with_validation(
        api="/collections/{collection_name}/points/query",
        method="POST",
        path_params={"collection_name": collection_name},
        body={
            "query": {
                "feedback": {
                    "target": [0.1, 0.2, 0.3, 0.4],
                    "feedback": [ {"vector": 1, "score": 0.85} ],
                    "strategy": {
                        "naive": {
                            "a": 0.12,
                            "b": -1.0,
                            "c": 0.99
                        }
                    }
                }
            }
        },
    )
    assert not response.ok, response.text
    assert response.json()["status"]["error"] == "Validation error in JSON body: [internal.query.feedback.strategy.b: value -1.0 invalid, must be 0.0 or larger]"
