"""Battle Damage Assessment (BDA) Structures."""
# pylint: disable=invalid-name,import-outside-toplevel

import concurrent.futures
import json
import random
import time
from dataclasses import dataclass, field
from enum import IntEnum
from os import environ, makedirs
from typing import Self

import config
import numpy as np
from ollama import ChatResponse, Client


class BDAEnum(IntEnum):
    """Base Enum for BDA Enums."""

    @property
    def text(self) -> str:
        """Returns the string representation of the field."""
        # ex. 0 -> "NO_DAMAGE" -> "no damage"
        return self.name.lower().replace("_", " ")

    @property
    def k_len(self):
        """Returns the total number of categories (K) in the Enum."""
        # NOTE: __members__ returns dictionary of Enum items
        return len(self.__class__.__members__)


class TargetType(BDAEnum):
    """IntEnum containing ordered collection of target types."""

    BRIDGES = 0
    BUILDINGS = 1
    MILITARY_EQUIPMENT = 7
    OBJECT_NOT_FOUND = 21
    UNKNOWN_HALLUCINATED = 99


class DamageBridge(BDAEnum):
    """IntEnum containing ordered collection of damage levels for bridges."""

    NO_DAMAGE = 0
    LIGHT_DAMAGE = 1
    MODERATE_DAMAGE = 2
    SEVERE_DAMAGE = 3
    DESTROYED = 4


class DamageBuildings(BDAEnum):
    """IntEnum containing ordered collection of damage levels for buildings."""

    NO_DAMAGE = 0
    LIGHT_DAMAGE = 1
    MODERATE_DAMAGE = 2
    SEVERE_DAMAGE = 3
    DESTROYED = 4


class DamageMilitaryEquipment(BDAEnum):
    """IntEnum containing ordered collection of damage levels for military equipment."""

    NO_DAMAGE = 0
    DAMAGED = 1
    DESTROYED = 2


class DamageNotFound(BDAEnum):
    """IntEnum containing damage level for images without doctrinal objects."""

    NOT_APPLICABLE = 0


class Confidence(BDAEnum):
    """IntEnum containing ordered collection of confidence levels."""

    POSSIBLE = 0
    PROBABLE = 1
    CONFIRMED = 2


target_damage_map = {
    "bridges": {"target_type": TargetType.BRIDGES, "damage_category": DamageBridge},
    "buildings": {
        "target_type": TargetType.BUILDINGS,
        "damage_category": DamageBuildings,
    },
    "military_equipment": {
        "target_type": TargetType.MILITARY_EQUIPMENT,
        "damage_category": DamageMilitaryEquipment,
    },
    "object_not_found": {
        "target_type": TargetType.OBJECT_NOT_FOUND,
        "damage_category": DamageNotFound,
    },
}


@dataclass
class BoundingBox:
    """Represents a 2D bounding box."""

    xmin: int
    ymin: int
    xmax: int
    ymax: int

    # Declare "area" property, but don't require at initialization
    area: int = field(init=False)

    def __post_init__(self):
        """Performs additional setup after __init__ is complete."""
        # Calculate and store the area of the bounding box.
        self.area = (self.xmax - self.xmin) * (self.ymax - self.ymin)

    def calc_iou(self, box: Self) -> float:
        """Calculates the Intersection over Union (IoU) for two bounding boxes.

        Args:
            box: BoundingBox instance.

        Returns:
            Value of IoU
        """
        intersection = self.intersect_area(box)
        union = self.area + box.area - intersection

        if union == 0:
            return 0.0

        return intersection / union

    def intersect_area(self, box: Self) -> int:
        """Calculates intersecting area of two bounding boxes.

        Args:
            box: BoundingBox instance.

        Returns:
            The area of the overlap or zero if boxes do not overlap.
        """
        # Check if t1 and t2 are completely disjoint
        if (
            box.xmax < self.xmin
            or box.xmin > self.xmax
            or box.ymin > self.ymax
            or box.ymax < self.ymin
        ):
            return 0

        # Determine intersecting rectangle:
        #     1. Find the min of ending x and y values
        #     2. Find the max of starting x and y values
        overlap_width = min(self.xmax, box.xmax) - max(self.xmin, box.xmin)
        overlap_height = min(self.ymax, box.ymax) - max(self.ymin, box.ymin)

        return overlap_width * overlap_height


@dataclass
class BDATarget:
    """Represents a Battle Damage Assessment report."""

    target_label: str
    target_type: TargetType
    damage_category: BDAEnum
    confidence: Confidence
    logic: str
    box: BoundingBox
    ndarray: np.ndarray


@dataclass
class BDAReportMetadata:
    """Contains the metadata of a BDA report."""

    model_name: str
    image_id: str
    image_filename: str
    date_created: str
    report_type: str
    analyst: str
    inference_time: str


@dataclass
class BDAMatch:
    """Represents a match between a reference and predicted BDA target."""

    ref_target: BDATarget
    pred_target: BDATarget
    iou: float
    w_i: float
    w_d: float
    w_c: float
    d_cost: float
    c_cost: float
    cost: float
    score_assess: float
    score_logic: float | None
    w_assess: float
    w_logic: float
    score: float | None


class BDAReport:
    """Manages a collection of BDA objects."""

    def __init__(self, metadata: BDAReportMetadata, targets: list[BDATarget]):
        """Init."""
        self.metadata = metadata
        self.targets = targets
        self.logs_path = "logs_llmaaj"

        makedirs(self.logs_path, exist_ok=True)

        # Build a matrix of BDAs (N rows x 3 columns):
        #     Column 0: Target Type | Column 1: Damage | Column 2: Confidence
        if targets:
            self.matrix = np.array([target.ndarray for target in targets])
        else:
            # Create empty matrix if no targets
            self.matrix = np.empty((0, 3))

    def filter_by_target(self, target_type: TargetType) -> list[BDATarget]:
        """Returns BDA objects matching a specific target type."""
        mask = self.matrix[:, 0] == target_type

        # NOTE: Mask is now a numpy boolean filter. Keep track of that?

        # If mask is true for a given BDA, add BDA to resulting list
        return [target for target, m in zip(self.targets, mask, strict=False) if m]

    def filter_by_bda(self, reference_bda: BDATarget) -> list[BDATarget]:
        """Finds all BDAs that share the same target type as the reference."""
        return self.filter_by_target(reference_bda.target_type)

    @classmethod
    def from_dict(cls, bda_dict: dict) -> Self:
        """Class factory method to create a BDA object from a dictionary.

        Args:
            bda_dict: BDA dictionary (with metadata, physical damage, functional damage, summary)

        Returns:
            Instantiated BDA class
        """
        # Get JSON report metadata and create BDAReportMetadata instance
        metadata_dict = bda_dict.get("metadata", {})
        metadata = BDAReportMetadata(
            model_name=metadata_dict.get("model_name", ""),
            image_id=metadata_dict.get("image_id", ""),
            image_filename=metadata_dict.get("image_filename", ""),
            date_created=metadata_dict.get("date_created", ""),
            report_type=metadata_dict.get("report_type", ""),
            analyst=metadata_dict.get("analyst", ""),
            inference_time=metadata_dict.get("inference_time", ""),
        )
        # Parse the report and extract detected objects
        target_list = []

        for target_label, target_data in bda_dict["physical_damage"].items():
            try:
                # Get inner dictionary from target_damage_map dictionary
                #     ex. td_map = { "target_type": ..., "damage_category": ... }
                target_type = TargetType[target_data["target_type"].upper().replace(" ", "_")]
                td_map = target_damage_map[target_data["target_type"]]

                damage_category = td_map["damage_category"][
                    target_data["damage_category"].upper().replace(" ", "_")
                ]

                confidence = Confidence[target_data["confidence_level"].upper().replace(" ", "_")]
            except KeyError as e:
                print(
                        f"[*] Unknown attribute {e} for {target_label} "
                        f"in {metadata.image_filename}. Marking as FP."
                    )

                target_type = TargetType.UNKNOWN_HALLUCINATED
                damage_category = DamageNotFound.NOT_APPLICABLE
                confidence = Confidence.POSSIBLE

            logic = target_data.get("brief_supporting_logic", "")

            try:
                if isinstance(target_data["bounding_box"], list):
                    box = BoundingBox(*target_data["bounding_box"])
                else:
                    box = BoundingBox(**target_data["bounding_box"])
            except TypeError:
                print(
                    f"[*] Error parsing bounding box for {target_label} in "
                    f"{metadata.image_filename}. Skipping."
                )
                continue

            # Convert BDA fields to numpy array for more efficient filtering/comparison
            ndarray = np.array([target_type, damage_category, confidence])

            # Return instantiated class
            target_list.append(
                BDATarget(
                    target_label=target_label,
                    target_type=target_type,
                    damage_category=damage_category,
                    confidence=confidence,
                    logic=logic,
                    box=box,
                    ndarray=ndarray,
                )
            )

        return cls(metadata=metadata, targets=target_list)

    def _llmaaj(
        self,
        ref_bda: BDATarget,
        pred_bda: BDATarget,
        client: Client,
        model: str = "qwen3-vl:235b-cloud",
    ) -> tuple | None:
        """Get LLMaaJ score and reasoning for match logic.

        Args:
            ref_bda: Reference BDATarget
            pred_bda: Predicted BDATarget
            client: Shared Ollama Client object
            model: Ollama Cloud model name

        Returns:
            Score generated via LLMaaJ, normalized, or None if the API fails.
            Also returns LLMaaJ reasoning for that score.
        """
        # print(f"[*] Human logic: {ref_bda.logic}\n")
        # print(f"[*] Model logic: {pred_bda.logic}\n")

        max_retries = 10

        query = f"""You are an expert military intelligence analyst acting as an impartial judge for an automated Battle Damage Assessment (BDA) pipeline.

Your task is to compare a human analyst's reference logic against an AI computer vision model's predicted logic.

### Evaluation Guidelines
1. Focus on the core functional state of the target (ex. no damage, damaged, destroyed).
2. Do not penalize the prediction for including extra observational details (ex. dirt, grime, minor cosmetic scorch marks) as long as the overall conclusion aligns with the reference.
3. A score of 0 should be reserved for fundamental contradictions regarding the severity of damage or the operability of the target (ex. Reference says "destroyed", Prediction says "intact").

Compare the reference text against the predicted text and grade the prediction using the following integer scale:
- 0: The predicted text fundamentally contradicts the core functional assessment of the reference text.
- 1: The predicted text agrees on the broad state of the target but misses some key reasoning or introduces minor deviations.
- 2: The predicted text fully aligns with the core reasoning and functional state of the reference, even if it uses different phrasing or adds minor, non-contradictory details.

<reference_logic>
{ref_bda.logic}
</reference_logic>

<predicted_logic>
{pred_bda.logic}
</predicted_logic>

Return a JSON object with the following schema:
{{
    "reasoning": "string",
    "score": integer
}}

The "reasoning" field must explain step-by-step why you chose the value for "score".
Output ONLY valid JSON.
"""

        # Connec to LLM (with exponential backoff)
        for attempt in range(max_retries):
            try:
                response: ChatResponse = client.chat(
                    model=model,
                    messages=[{"role": "user", "content": query}],
                    format="json",
                    options={"temperature": 0.0},  # For deterministic result
                )

                # Parse the JSON string returned by the model
                if response.message.content is not None:
                    result = json.loads(response.message.content)
                else:
                    result = {}

                # Extract the score (default to 0 if something goes wrong)
                score = result.get("score", 0)

                # print(f"\t[*] LLMaaJ: {result.get('reasoning')}")

                # Normalize the 0, 1, 2 integer into a 0.0, 0.5, 1.0 float
                return float(score) / 2.0, result.get("reasoning")
            except Exception as e:
                error_msg = str(e).lower()

                if isinstance(e, json.JSONDecodeError):
                    print("[*] LLM returned invalid JSON. Returning None.")
                    return None

                if any(
                    err in error_msg
                    for err in ["429", "too many requests", "timeout", "50"]
                ):
                    # Exponential Backoff: 1s, 2s, 4s, 8s (with addt'l jitter)
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)

                    print(
                        f"[*] Cloud usage error. Retrying in {sleep_time:.2f} seconds..."
                    )

                    time.sleep(sleep_time)
                    continue

                # Handle miscellaneous errors
                print(f"[*] Unhandled LLMaaJ error: {e}")
                return None

        # Attempts exhausted
        print("[*] Max retries reached querying LLM. Returning None.")

        return None

    def _log_llmaaj(
        self, R: Self, match: BDAMatch, llmaaj_score: float, llmaaj_evaluation: str
    ) -> None:
        """Appends LLMaaJ evaluation results to both JSONL and text logs.

        Args:
            R: The BDAReport containing human assessments.
            match: A BDAMatch object.
            llmaaj_score: Float score generated by the LLMaaJ
            llmaaj_evaluation: String evaluation generated by the LLMaaJ

        Returns:
            None
        """
        assert config.OUTPUT_DIR is not None, "[*] Output folder not initialized."
        output_path = config.OUTPUT_DIR / "logs_llmaaj"
        output_path.mkdir(parents=True, exist_ok=True)

        log_data = {
            "Image Filename": R.metadata.image_filename,
            "Reference Target": match.ref_target.target_label,
            "Model Target": match.pred_target.target_label,
            "Reference Logic": match.ref_target.logic,
            "Model Logic": match.pred_target.logic,
            "LLMaaJ Score": llmaaj_score,
            "LLMaaJ Evaluation": llmaaj_evaluation,
        }

        # Save LLMaaJ logs in both JSONL and human-readable formats
        with (
            open(f"{output_path}/llmaaj.jsonl", "a", encoding="utf-8") as jsonl_file,
            open(f"{output_path}/llmaaj.log", "a", encoding="utf-8") as log_file,
        ):
            jsonl_file.write(json.dumps(log_data) + "\n")
            log_file.write(json.dumps(log_data, indent=4) + "\n\n")

            print(
                f"    | {log_data['Image Filename']} |"
                f" R-{log_data['Reference Target']} |"
                f" P-{log_data['Model Target']} | ---> "
                f"{log_data['LLMaaJ Score']}"
            )

    def _calculate_target_score(
        self,
        score_assess: float,
        score_logic: float | None,
        w_assess: float = 0.7,
    ) -> float | None:
        """Calculates final object score.

        Args:
            score_assess: Object detection/assessment score.
            score_logic: Assessment logic score (can be None on error).
            w_assess: Relative weight of the assessment component score.

        Returns:
            Final normalized target score, or None if logic assessment failed.
        """
        if score_logic is None:
            return None

        # Weights should add up to one
        w_logic = 1.0 - w_assess

        # Scale the target score with `score_assess`:
        #   Case 1: score_assess=1.0, score_logic=1.0 --> 1.0
        #   Case 2: score_assess=1.0, score_logic=0.0 --> 0.7 (if w_assess == 0.7)
        #   Case 3: score_assess=0.0, score_logic=1.0 --> 0.0
        #   Case 4: score_assess=0.5, score_logic=1.0 --> 0.5

        return (w_assess * score_assess) + (w_logic * score_logic)

    def _evaluate_logic(self, R, matches: list[BDAMatch]):
        """Evaluates BDAMatch logic concurrently (updating in-place).

        Args:
            R: The BDAReport containing human assessments.
            matches: List of BDAMatch objects.
        """
        api_key = environ.get("OLLAMA_API_KEY")
        if not api_key:
            raise KeyError("[*] Environment variable 'OLLAMA_API_KEY' not set.")

        timeout_secs = 60 * 15

        # Share Client object between match queries
        shared_client = Client(
            host="https://ollama.com",
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            timeout=timeout_secs,
        )

        # Use a ThreadPool to run requests concurrently
        # `max_workers`` helps us keep Ollama Cloud happy
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            # Dictionary to keep track of which future belongs to which match
            future_to_match = {
                executor.submit(
                    self._llmaaj, match.ref_target, match.pred_target, shared_client
                ): match
                for match in matches
            }

            # As each concurrent request finishes, record the score
            for future in concurrent.futures.as_completed(future_to_match):
                match = future_to_match[future]

                try:
                    # Get the returned score and evaluation from _llmaaj
                    result = future.result()
                    if result is None:
                        raise Exception("unable to contact LLM provider.")
                    else:
                        score, evaluation = result
                        match.score_logic = score

                        # Log evaluation to file
                        self._log_llmaaj(R, match, score, evaluation)
                except Exception as e:
                    print(f"[*] LLMaaJ operation generated an exception: {e}")

    def get_bda_matches(
        self,
        R: Self,
        min_iou: float = 0.001,
        w_i: float = 0.4,
        w_assess: float = 0.7,
    ) -> tuple[list[BDAMatch], list[BDATarget], list[BDATarget]] | None:
        """Pairs predictions to reference BDAs using the Hungarian Algorithm.

        The primary metric is IoU. Normalized ordinal distance of damage and
        confidence are used as weighted tiebreakers.

        Args:
            R: The BDAReport containing human assessments.
            min_iou: Minimum IoU required to consider a match valid.
            w_i: Weight of the IoU (bounding box) cost.
            w_assess: Relative weight of the assessment component score.

        Returns:
            Tuple of matched BDAs, False Positives, and False Negatives.
        """
        # Lazy load
        from scipy.optimize import linear_sum_assignment

        matches = []
        max_cost = 1e5

        # Cost weights (should add up to one)
        w_d = (1 - w_i) / 2
        w_c = 1 - w_i - w_d

        # Component score weights (i.e. Assessment, Logic) should add up to one
        w_logic = 1 - w_assess

        if len(R.targets) == 0:
            return None

        # Find unique target types in R (ex. [bridge bridge tank bridge] -> [bridge tank])
        unique_target_types = np.unique(R.matrix[:, 0])

        # Iterate through each target type and apply Hungarian Algorithm
        for target_type in unique_target_types:
            t_enum = TargetType(target_type)

            # Look at objects with the same target type only
            P_filtered = self.filter_by_target(t_enum)
            R_filtered = R.filter_by_target(t_enum)

            n = len(P_filtered)
            m = len(R_filtered)

            if n == 0 or m == 0:
                continue

            # Initialize the N x M Multi-Objective Cost Matrix
            cost_matrix = np.zeros((n, m), dtype=float)

            # For every target in P, compare against R and build Cost Matrix
            for i, P_target in enumerate(P_filtered):
                for j, R_target in enumerate(R_filtered):
                    # Calculate the base cost (i.e. IoU between targets, inverted)
                    iou = P_target.box.calc_iou(R_target.box)

                    if iou >= min_iou:
                        cost_iou = 1.0 - iou

                        # Subcost 1: Normalized Damage Cost (no longer subtracted from one)
                        #     K = number of damage levels for target_R
                        #         Dynamically find K by checking the length of the Enum
                        k = R_target.damage_category.k_len
                        c_d = abs(
                            P_target.damage_category.value
                            - R_target.damage_category.value
                        ) / max(1, k - 1)

                        # Subcost 2: Normalized Confidence Cost
                        # NOTE: Confidence always has 3 levels (0, 1, 2), so max distance is 2
                        c_c = (
                            abs(P_target.confidence.value - R_target.confidence.value)
                            / 2.0
                        )

                        # Total (weighted) cost
                        cost_matrix[i, j] = (w_i * cost_iou) + (w_d * c_d) + (w_c * c_c)
                    else:
                        # IoU doesn't meet threshold IoU
                        cost_matrix[i, j] = max_cost

            # Run the Hungarian Algorithm on this specific subset (mathmagic)
            P_indices, R_indices = linear_sum_assignment(cost_matrix)

            # Assemble the matched pairs (filtering out invalid boxes)
            for p_idx, r_idx in zip(P_indices, R_indices, strict=False):
                p_bda = P_filtered[p_idx]
                r_bda = R_filtered[r_idx]

                # Check the raw IoU to ensure they actually overlap
                # Necessary because linear_sum_assignment may still pair to a terrible match
                actual_iou = p_bda.box.calc_iou(r_bda.box)

                if actual_iou >= min_iou:
                    # Recalculate c_c and d_c for successful match
                    k = r_bda.damage_category.k_len
                    c_d = abs(
                        p_bda.damage_category.value - r_bda.damage_category.value
                    ) / max(1, k - 1)
                    c_c = abs(p_bda.confidence.value - r_bda.confidence.value) / 2.0

                    score_assess = 1 - cost_matrix[p_idx, r_idx].item()

                    matches.append(
                        BDAMatch(
                            ref_target=r_bda,
                            pred_target=p_bda,
                            cost=cost_matrix[p_idx, r_idx].item(),
                            iou=actual_iou,
                            w_i=w_i,
                            w_d=w_d,
                            w_c=w_c,
                            d_cost=c_d,
                            c_cost=c_c,
                            score_assess=score_assess,
                            score_logic=0,
                            w_assess=w_assess,
                            w_logic=w_logic,
                            score=0,
                        )
                    )
                else:
                    if t_enum == TargetType.OBJECT_NOT_FOUND:
                        matches.append(
                            BDAMatch(
                                ref_target=r_bda,
                                pred_target=p_bda,
                                cost=0,
                                iou=0,
                                w_i=w_i,
                                w_d=w_d,
                                w_c=w_c,
                                d_cost=0,
                                c_cost=0,
                                score_assess=0,
                                score_logic=0,
                                w_assess=0,
                                w_logic=0,
                                score=0,
                            )
                        )

        # Query LLMaaJ for every matched pair (that's not OBJECT_NOT_FOUND)
        matches_valid = [match for match in matches if match.score_assess > 0.0]

        print("\n[*] Submitting matches to LLMaaJ:\n")
        self._evaluate_logic(R, matches_valid)

        # Finish populating the `score` value for every match
        for match in matches:
            match.score = self._calculate_target_score(
                match.score_assess,
                match.score_logic,
                w_assess,
            )

        # Determine False Positives and False Negatives
        # Start by gettings memory addresses of all matched BDATargets (to filter out)
        # We use memory addresses instead of defining BDATarget equality (maybe later)
        ref_match_ids = {id(match.ref_target) for match in matches}
        pred_match_ids = {id(match.pred_target) for match in matches}

        false_negatives = [r for r in R.targets if id(r) not in ref_match_ids]
        false_positives = [p for p in self.targets if id(p) not in pred_match_ids]

        return matches, false_negatives, false_positives


class SceneReport:
    """Stores score data for a particular scene."""

    def __init__(
        self,
        model_name: str,
        image_filename: str,
        matches: list[BDAMatch],
        count_targets: int,
        count_fn: int,
        count_fp: int,
        inference_time: float = 0.0,
    ):
        """Init."""
        self.model_name = model_name
        self.image = image_filename
        self.count_targets = count_targets
        self.count_fn = count_fn
        self.count_fp = count_fp
        self.inference_time = inference_time
        self.sum_assess = 0.0
        self.sum_logic = 0.0
        self.sum_total = 0.0
        self.assess = 0.0
        self.logic = 0.0
        self.total = 0.0

        self._calc_scores(matches)

    def _calc_scores(self, matches: list[BDAMatch]) -> None:
        """Calculate scores for a particular scene.

        Args:
            matches: List of BDAMatch objects
        """
        # Calculate sums
        for match in matches:
            self.sum_assess += match.score_assess

            if match.score_logic is not None:
                self.sum_logic += match.score_logic

            if match.score is not None:
                self.sum_total += match.score

        # denominator == TP + FN + FP
        denominator = self.count_targets + self.count_fp

        # Calculate averages
        if denominator > 0:
            self.assess = self.sum_assess / denominator
            self.total = self.sum_total / denominator

            # Logic only applies to objects that actually exist so we don't penalize with FPs
            if self.count_targets > 0 and len(matches) > 0:
                self.logic = self.sum_logic / self.count_targets
            else:
                self.logic = None


class ModelReport:
    """Calculates the overall score for the tested model."""

    def __init__(self, scene_reports: list[SceneReport]):
        """Init.

        Args:
            scene_reports: List of SceneReport objects
        """
        self.model_name = scene_reports[0].model_name

        self.model_sum_assess = 0.0
        self.model_sum_logic = 0.0
        self.model_sum_total = 0.0

        self.model_targets = 0
        self.model_fp = 0
        self.model_fn = 0

        self.total_inference_time = 0.0

        # Store the number of images for this batch
        self.image_count = len(scene_reports)

        # Calculate totals independently across all images
        for scene in scene_reports:
            self.model_sum_assess += scene.sum_assess
            self.model_sum_logic += scene.sum_logic
            self.model_sum_total += scene.sum_total

            self.model_targets += scene.count_targets
            self.model_fp += scene.count_fp
            self.model_fn += scene.count_fn

            # Accumulate total time
            self.total_inference_time += getattr(scene, "inference_time", 0.0)

        # Denominator == TP + FN + FP (across all images)
        denominator = self.model_targets + self.model_fp

        if denominator > 0:
            self.model_score_assess = self.model_sum_assess / denominator
            self.model_score_total = self.model_sum_total / denominator
        else:
            self.model_score_assess = 0.0
            self.model_score_total = 0.0

        # Logic Denominator == TP + FN (ignore FP for fairer calc)
        if self.model_targets > 0:
            self.model_score_logic = self.model_sum_logic / self.model_targets
        else:
            self.model_score_logic = None

        # Calculate average inference time
        if self.image_count > 0:
            self.avg_inference_time = self.total_inference_time / self.image_count
        else:
            self.avg_inference_time = 0.0

    def print_summary(self) -> None:
        """Prints the final model scores."""
        print(f"\n{'=' * 45}")
        print(f"{'OVERALL MODEL SCORE':^45}")
        print("=" * 45)
        print(f"{'Total Reference Targets ':>34}: {self.model_targets:>5}")
        print(f"{'Total False Negatives (Missed) ':>34}: {self.model_fn:>5}")
        print(f"{'Total False Positives (Halluc) ':>34}: {self.model_fp:>5}")
        print(f"{'Avg Inference Time/Img ':>34}: {self.avg_inference_time:>4.2f}s")
        print("-" * 45)

        print(f"{'OVERALL ASSESS SCORE ':>34}: {self.model_score_assess:.3f}")

        if self.model_score_logic is not None:
            print(f"{'OVERALL LOGIC SCORE ':>34}: {self.model_score_logic:.3f}")
        else:
            print(f"{'OVERALL LOGIC SCORE ':>34}:   N/A")

        print(f"{'OVERALL TOTAL SCORE ':>34}: {self.model_score_total:.3f}")
        print("=" * 45 + "\n")

    def to_dict(self) -> dict:
        """Return dictionary-based ModelReport."""
        return {
            "model_name": self.model_name,
            "count_target": self.model_targets,
            "count_fn": self.model_fn,
            "count_fp": self.model_fp,
            "inference_time_avg": self.avg_inference_time,
            "assess_avg": self.model_score_assess,
            "logic_avg": self.model_score_logic,
            "total_avg": self.model_score_total,
        }
