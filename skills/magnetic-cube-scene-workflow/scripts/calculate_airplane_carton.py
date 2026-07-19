from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


CUBE_WEIGHT_KG = 0.0025
COLOR_BOX_WEIGHT_KG = 0.070
GROSS_ALLOWANCE_KG = 1.5
MAX_GROSS_KG = 22.0
QUANTITY_MULTIPLE = 12
FIRST_TIER_CARTON_QUANTITY = 36

CORRUGATION_CM = 0.6
LOGISTICS_CLEARANCE_CM = 0.5
BOX_DIRECTION_ALLOWANCE_CM = 0.25
MIN_OUTER_HEIGHT_CM = 40.0
TARGET_OUTER_HEIGHT_CM = 55.0
MAX_OUTER_HEIGHT_CM = 78.0
MAX_OUTER_LENGTH_CM = 91.44
MAX_OUTER_WIDTH_CM = 60.0


@dataclass(frozen=True)
class Result:
    name: str
    pcs: int
    color_box_cm: tuple[float, float, float]
    packed_box_weight_kg: float
    carton_quantity: int
    exact_packed_carton_weight_kg: float
    declared_net_weight_kg: float
    declared_gross_weight_kg: float
    arrangement: tuple[int, int, int]
    carton_cm: tuple[float, float, float]


def round_up_half(value: float) -> float:
    return math.ceil((value - 1e-9) * 2) / 2


def color_box_for_pcs(
    pcs: int, *, allow_legacy_below_80: bool = False
) -> tuple[float, float, float]:
    if pcs <= 0 or pcs > 198 or (pcs < 80 and not allow_legacy_below_80):
        raise ValueError("PCS must be between 80 and 198")
    if pcs <= 120:
        return (19.5, 15.5, 4.5)
    if pcs <= 160:
        return (21.5, 17.5, 4.5)
    return (23.5, 19.5, 4.5)


def carton_weight_options(
    pcs: int,
) -> tuple[float, list[tuple[int, float, float, float]]]:
    packed_box_weight = pcs * CUBE_WEIGHT_KG + COLOR_BOX_WEIGHT_KG
    valid: list[tuple[int, float, float, float]] = []
    quantities = (
        [FIRST_TIER_CARTON_QUANTITY]
        if pcs <= 120
        else range(QUANTITY_MULTIPLE, 1000, QUANTITY_MULTIPLE)
    )
    for quantity in quantities:
        exact = packed_box_weight * quantity
        declared_net = round_up_half(exact)
        declared_gross = declared_net + GROSS_ALLOWANCE_KG
        if declared_gross <= MAX_GROSS_KG:
            valid.append((quantity, exact, declared_net, declared_gross))
    if not valid:
        raise ValueError(f"No valid 12-multiple carton quantity for {pcs} PCS")
    return packed_box_weight, valid


def html_carton_layout(
    color_box: tuple[float, float, float], quantity: int
) -> tuple[tuple[int, int, int], tuple[float, float, float]]:
    length, width, height = color_box
    padding = CORRUGATION_CM + LOGISTICS_CLEARANCE_CM
    orientations = (
        ("HxLxW", (height, length, width)),
        ("HxWxL", (height, width, length)),
    )

    for _, units in orientations:
        candidates: list[
            tuple[float, tuple[int, int, int], tuple[float, float, float]]
        ] = []
        for length_count in range(1, quantity + 1):
            for row_count in range(1, quantity + 1):
                per_layer = length_count * row_count
                if quantity % per_layer:
                    continue
                layer_count = quantity // per_layer
                counts = (length_count, row_count, layer_count)
                inner = tuple(
                    count * (unit + BOX_DIRECTION_ALLOWANCE_CM)
                    for count, unit in zip(counts, units)
                )
                outer_l, outer_w, outer_h = tuple(
                    round_up_half(value + padding) for value in inner
                )
                if outer_l <= outer_w or outer_h <= outer_w:
                    continue
                if not 22.0 <= outer_w <= MAX_OUTER_WIDTH_CM:
                    continue
                if not MIN_OUTER_HEIGHT_CM <= outer_h <= MAX_OUTER_HEIGHT_CM:
                    continue
                if outer_l > MAX_OUTER_LENGTH_CM:
                    continue

                aspect_ratio = max(outer_l, outer_h) / min(outer_l, outer_h)
                overall_ratio = max(outer_l, outer_h) / outer_w
                if aspect_ratio > 2.5 or overall_ratio > 2.5:
                    continue

                penalty = 50 if aspect_ratio > 1.8 else 0
                score = (
                    100
                    - abs(1 - aspect_ratio) * 30
                    - abs(outer_h - TARGET_OUTER_HEIGHT_CM) * 0.5
                    - max(0, overall_ratio - 1) * 10
                    - penalty
                )
                candidates.append((score, counts, (outer_l, outer_w, outer_h)))

        if candidates:
            # Python max keeps the first layout on a score tie, matching the
            # HTML's stable Array.sort over the same loop order.
            _, arrangement, carton = max(candidates, key=lambda item: item[0])
            return arrangement, carton

    raise ValueError("No carton layout satisfies the supplied HTML constraints")


def calculate(
    name: str, pcs: int, *, allow_legacy_below_80: bool = False
) -> Result:
    color_box = color_box_for_pcs(
        pcs, allow_legacy_below_80=allow_legacy_below_80
    )
    box_weight, weight_options = carton_weight_options(pcs)
    selected = None
    for quantity, exact, declared_net, declared_gross in reversed(weight_options):
        try:
            arrangement, carton = html_carton_layout(color_box, quantity)
        except ValueError:
            continue
        selected = (
            quantity,
            exact,
            declared_net,
            declared_gross,
            arrangement,
            carton,
        )
        break
    if selected is None:
        raise ValueError(
            f"No valid 12-multiple carton quantity and layout for {pcs} PCS"
        )
    (
        quantity,
        exact,
        declared_net,
        declared_gross,
        arrangement,
        carton,
    ) = selected
    return Result(
        name=name,
        pcs=pcs,
        color_box_cm=color_box,
        packed_box_weight_kg=round(box_weight, 4),
        carton_quantity=quantity,
        exact_packed_carton_weight_kg=round(exact, 4),
        declared_net_weight_kg=declared_net,
        declared_gross_weight_kg=declared_gross,
        arrangement=arrangement,
        carton_cm=carton,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate locked magnetic-cube airplane-box carton data")
    parser.add_argument("pcs", type=int)
    parser.add_argument("--name", default="")
    parser.add_argument(
        "--allow-legacy-below-80",
        action="store_true",
        help="Allow an existing audited SKU below 80 PCS; never use for new scenes",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            asdict(
                calculate(
                    args.name,
                    args.pcs,
                    allow_legacy_below_80=args.allow_legacy_below_80,
                )
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
