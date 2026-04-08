"""Export test suite."""

import copy
from datetime import datetime
import json
from pathlib import Path
import pytest
import re

from bda_svc import export


@pytest.fixture
def metadata_std(tmp_path):
    return {
        "image_path": tmp_path / "image42.png",
        "model_name": "qwen3",
        "inference_time": 3.14,
    }


def get_bda_template():
    return copy.deepcopy({
        "metadata": { 
            "model_name": "", 
            "image_id": "", 
            "image_filename": "", 
            "date_created": "", 
            "location": {
                "crs": "",
                "coordinates": ""
            }, 
            "report_type": "PDA", 
            "analyst": "bda-svc", 
            "inference_time": "", 
        }, 
        "physical_damage": {
            "target_0": {}
        }, 
        "summary": "---TEST SUMMARY---",
    })


# ---------------------------------------------------------------------------
# Test: Export Folder Validation (build_report)
# ---------------------------------------------------------------------------


def _test_bda(bda_std, bda_to_test):
    """Test contents of one BDA against another BDA."""
    assert isinstance(bda_to_test["metadata"], dict)
    assert bda_to_test["metadata"]["model_name"] == bda_std["metadata"]["model_name"]

    # Validate that `image_id` is a valid UUID4 value
    regex = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
    uuid4_valid = re.search(regex, bda_to_test["metadata"]["image_id"])

    assert uuid4_valid is not None

    assert bda_to_test["metadata"]["image_filename"] == bda_std["metadata"]["image_path"].name
    assert datetime.fromisoformat(bda_to_test["metadata"]["date_created"])
    assert isinstance(bda_to_test["metadata"]["location"], dict)
    assert bda_to_test["metadata"]["report_type"] == "PDA"
    assert bda_to_test["metadata"]["analyst"] == "bda-svc"
    assert bda_to_test["metadata"]["inference_time"] == f"{bda_std['metadata']['inference_time']:.2f}"
    assert bda_to_test["physical_damage"] == bda_std["physical_damage"]
    assert bda_to_test["summary"] == bda_std["summary"]


def test_build_report(metadata_std):
    """Test if our partial BDA gets converted to a full BDA."""
    # Build the BDA to compare to
    bda_std = get_bda_template()
    bda_std["metadata"].update(metadata_std)

    bda_to_test = export.build_report(bda_std, **metadata_std)

    _test_bda(bda_std, bda_to_test)


# ---------------------------------------------------------------------------
# Test: Export Folder Validation (save_json)
# ---------------------------------------------------------------------------

def test_save_json(tmp_path, metadata_std):
    """Test if valid JSON file created."""
    bda_std = get_bda_template()
    bda_std["metadata"].update(metadata_std)

    json_path = export.save_json(bda_std, output_path=tmp_path, **metadata_std)
    
    assert isinstance(json_path, Path)

    with json_path.open("r", encoding="utf-8") as file:
        bda_to_test = json.load(file)

        _test_bda(bda_std, bda_to_test)