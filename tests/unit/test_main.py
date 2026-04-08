"""Test main entrypoint."""

from bda_svc import app
import pytest


def test_main(mocker, capsys):
    """Test main entrypoint."""
    # Mock CLI arguments
    mock_args = mocker.Mock()
    mock_args.input = "image42.png"
    mock_args.output = "/path/to/nowhere"
    mocker.patch("bda_svc.app.cli.get_args", return_value=mock_args)

    # Mock input folder/files
    mock_inputs = mocker.Mock()
    mocker.patch("bda_svc.app.inputs.get_input_folder", return_value=".")
    mocker.patch("bda_svc.app.inputs.get_input_paths", return_value=[mock_args.input])

    # Mock BDAPipeline
    mock_pipeline_class = mocker.patch("bda_svc.app.BDAPipeline")
    mock_pipeline_instance = mock_pipeline_class.return_value          # Another Mock object
    mock_pipeline_instance.detection_vlm.model = "FakeModel3"
    mock_pipeline_instance.assessment_vlm.model = "FakeModel3"
    mock_pipeline_instance.analyze.return_value = {"status": "success"}

    # Mock JSON save
    mock_save_json = mocker.patch("bda_svc.app.export.save_json")

    app.main()

    # Test exception logic
    mock_save_json.side_effect = Exception("fake path.")

    app.main()