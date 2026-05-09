# pp045b Rule Spec

```json
{
  "rule_id": "pp045b_tiny_upper_right_sparse_military_probe",
  "family": "tiny_sparse_military_equipment_context",
  "target_type": "military_equipment",
  "image_area_ratio_max": 0.00115,
  "military_equipment_count_min": 2,
  "military_equipment_count_max": 4,
  "center_x_ratio_min": 0.75,
  "center_y_ratio_max": 0.4,
  "uses_reference_or_eval_fields_at_inference": false,
  "deployability_caveat": "Simulation-only until removed case-28 boxes receive visual review.",
  "metrics": {
    "matches": 181,
    "false_negatives": 38,
    "false_positives": 15,
    "image_count": 117,
    "combined_errors": 53
  },
  "removals": [
    {
      "case_id": "28",
      "image_filename": "28.jpg",
      "removed_label": "target_1",
      "removed_target_type": "military_equipment",
      "removed_bbox": [
        1018.0,
        145.0,
        1052.0,
        176.0
      ],
      "image_area_ratio": 0.0011436631944444445,
      "center_x_ratio": 0.80859375,
      "center_y_ratio": 0.22291666666666668,
      "military_equipment_count": 4,
      "reason_removed": "tiny upper-right sparse military-equipment prediction",
      "after_the_fact_eval_status": "FP",
      "source_stage": "after_pp044a"
    },
    {
      "case_id": "28",
      "image_filename": "28.jpg",
      "removed_label": "target_2",
      "removed_target_type": "military_equipment",
      "removed_bbox": [
        1039.0,
        104.0,
        1069.0,
        135.0
      ],
      "image_area_ratio": 0.0010091145833333334,
      "center_x_ratio": 0.8234375,
      "center_y_ratio": 0.16597222222222222,
      "military_equipment_count": 4,
      "reason_removed": "tiny upper-right sparse military-equipment prediction",
      "after_the_fact_eval_status": "FP",
      "source_stage": "after_pp044a"
    },
    {
      "case_id": "28",
      "image_filename": "28.jpg",
      "removed_label": "target_3",
      "removed_target_type": "military_equipment",
      "removed_bbox": [
        1047.0,
        76.0,
        1066.0,
        99.0
      ],
      "image_area_ratio": 0.00047417534722222224,
      "center_x_ratio": 0.825390625,
      "center_y_ratio": 0.12152777777777778,
      "military_equipment_count": 4,
      "reason_removed": "tiny upper-right sparse military-equipment prediction",
      "after_the_fact_eval_status": "FP",
      "source_stage": "after_pp044a"
    }
  ]
}
```
