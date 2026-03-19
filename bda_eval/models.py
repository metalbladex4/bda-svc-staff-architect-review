"""Battle Damage Assessment (BDA) Structures."""
#pylint: disable=invalid-name,import-outside-toplevel

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Self

import numpy as np


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
    MILITARY_EQUIPMENT = 7
    OBJECT_NOT_FOUND = 21


class DamageBridge(BDAEnum):
    """IntEnum containing ordered collection of damage levels for bridges."""
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
    NA = 0


class Confidence(BDAEnum):
    """IntEnum containing ordered collection of confidence levels."""
    POSSIBLE = 0
    PROBABLE = 1
    CONFIRMED = 2


target_damage_map = {
    "bridges": {
        "target_type": TargetType.BRIDGES,
        "damage_category": DamageBridge
    },
    "military_equipment": {
        "target_type": TargetType.MILITARY_EQUIPMENT,
        "damage_category": DamageMilitaryEquipment
    },
    "object_not_found": {
        "target_type": TargetType.OBJECT_NOT_FOUND,
        "damage_category": DamageNotFound
    }
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
        #Calculate and store the area of the bounding box.
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
        if box.xmax < self.xmin or \
            box.xmin > self.xmax or \
            box.ymin > self.ymax or \
            box.ymax < self.ymin:
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


@dataclass
class BDAMatch:
    """"Represents a match between a reference and predicted BDA target."""
    ref_target: BDATarget
    pred_target: BDATarget
    cost: float
    iou: float


class BDAReport:
    """Manages a collection of BDA objects."""
    def __init__(self, metadata: BDAReportMetadata, targets: list[BDATarget]):
        """Init."""
        self.metadata = metadata
        self.targets = targets

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
            analyst=metadata_dict.get("analyst", "")
        )

        # Parse the report and extract detected objects
        target_list = []

        for target_label, target_data in bda_dict["physical_damage"].items():
            # Get inner dictionary from target_damage_map dictionary
            #     ex. td_map = { "target_type": ..., "damage_category": ... }
            td_map = target_damage_map[target_data["target_type"]]

            # Store BDA fields as IntEnum-subclassed objects
            target_type = td_map["target_type"]
            damage_category = \
                td_map["damage_category"][target_data["damage_category"].upper().replace(" ", "_")]
            confidence = Confidence[target_data["confidence_level"].upper()]

            logic = target_data["brief_supporting_logic"]
            box = BoundingBox(**target_data["bounding_box"])

            # Convert BDA fields to numpy array for more efficient filtering/comparison
            ndarray = np.array([
                target_type,
                damage_category,
                confidence
            ])

            # Return instantiated class
            target_list.append(BDATarget(
                target_label=target_label,
                target_type=target_type,
                damage_category=damage_category,
                confidence=confidence,
                logic=logic,
                box=box,
                ndarray=ndarray
            ))

        return cls(metadata=metadata, targets=target_list)

    def get_bda_matches(
        self,
        R: Self,
        min_iou: float = 0.001,
        w_d: float = 0.05,
        w_c: float = 0.05
    ) -> tuple[list[BDAMatch], list[BDATarget], list[BDATarget]] | None:
        """Pairs predictions to reference BDAs using the Hungarian Algorithm.

        The primary metric is IoU. Normalized ordinal distance of damage and
        confidence are used as weighted tiebreakers.

        Args:
            R: The BDAReport containing human assessments.
            min_iou: Minimum IoU required to consider a match valid.
            w_d: Weight of the damage penalty tiebreaker.
            w_c: Weight of the confidence penalty tiebreaker.

        Returns:
            Tuple of matched BDAs, False Positives, and False Negatives.
        """
        # Lazy load
        from scipy.optimize import linear_sum_assignment

        matches = []
        max_cost = 1e5

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
                        base_cost = 1.0 - iou

                        # Subcost 1: Normalized Damage Cost (no longer subtracted from one)
                        #     K = number of damage levels for target_R
                        #         Dynamically find K by checking the length of the Enum
                        k = R_target.damage_category.k_len
                        c_d = abs(P_target.damage_category.value - R_target.damage_category.value)\
                            / max(1, k - 1)

                        # Subcost 2: Normalized Confidence Cost
                        # NOTE: Confidence always has 3 levels (0, 1, 2), so max distance is 2
                        c_c = abs(P_target.confidence.value - R_target.confidence.value) / 2.0

                        # Total (weighted) cost
                        cost_matrix[i, j] = base_cost + (w_d * c_d) + (w_c * c_c)
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
                    matches.append(BDAMatch(
                        ref_target=r_bda,
                        pred_target=p_bda,
                        cost=cost_matrix[p_idx, r_idx].item(),
                        iou=actual_iou
                    ))
                else:
                    if t_enum == TargetType.OBJECT_NOT_FOUND:
                        matches.append(BDAMatch(
                            ref_target=r_bda,
                            pred_target=p_bda,
                            cost=0,
                            iou=0
                        ))

        # Determine False Positives and False Negatives
        # Start by gettings memory addresses of all matched BDATargets (to filter out)
        # We use memory addresses instead of defining BDATarget equality (maybe later)
        ref_match_ids = {id(match.ref_target) for match in matches}
        pred_match_ids = {id(match.pred_target) for match in matches}

        false_negatives = [r for r in R.targets if id(r) not in ref_match_ids]
        false_positives = [p for p in self.targets if id(p) not in pred_match_ids]

        return matches, false_negatives, false_positives
