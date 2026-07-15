# Packaging And Formula Rules

## Cube And Box Size

- Magnetic cube size: `2cm x 2cm x 2cm`.
- Magnetic cubes connect into compact rows. The airplane-box width is based on
  five connected cubes plus clearance.
- Use these locked finished outside airplane-box dimensions (`L x W x H`):
  - Up to `120 PCS`, including retained legacy samples below 80 PCS:
    `17.5 x 11 x 7cm`.
  - `121-160 PCS`: `23.5 x 11 x 7cm`.
  - `161-200 PCS`: `23.5 x 11 x 9cm`.
- The production scene range remains `80-200 PCS`. The below-80 exception only
  allows existing audited SKUs to use the smallest box; it does not permit new
  below-80 scene generation.
- Dimensions shown on the sheet must be outside the color box with straight dimension lines.

## Carton Quantity

Use the user's fixed rule:

- One cube weight: `0.0025kg`.
- One finished color box weight: `0.070kg`.
- Carton quantity must be a multiple of `12`.
- Exact packed-box weight = `pcs * 0.0025 + 0.070` kg.
- Exact packed-carton weight before the master-carton allowance =
  `exact packed-box weight * carton quantity`.
- Declared net weight is that exact value rounded upward to the next `0.5kg`.
  This conservative rounding is required because a 12-multiple quantity will
  generally not produce an exact integer or half-kilogram result.
- Declared gross weight = declared net weight + `1.5kg`.
- Choose the largest multiple of `12` where declared gross weight is `<=22kg`.
- Under this user-specific convention, declared net weight includes the 70g
  color box. Label it as packed-goods net weight internally; customs pure net
  weight would require a separate cube-only calculation.

Use `scripts/calculate_airplane_carton.py` instead of rewriting these formulas.

## HTML Carton Algorithm

Match `D:/Users/Administrator/Desktop/整合系统.html`:

- Five-layer BC corrugation thickness: `0.6cm`.
- International-logistics clearance: `0.5cm`.
- Add `0.25cm` per color box in every packed direction.
- Airplane-box orientation maps color-box `H` to the placement length axis,
  color-box `L` to the horizontal axis, and color-box `W` to the vertical axis.
- Accept only layouts where `length-count * row-count * layer-count` equals the
  carton quantity exactly.
- Add corrugation and clearance, then round every carton dimension upward to an
  integer or `0.5cm`.
- Label the largest finished dimension as carton length. Sort the remaining two
  so width is the smaller and height is the larger.
- Enforce the HTML limits: height `40-78cm`, width at most `60cm`, length at
  most `91.44cm`, and reject length/height ratios above `2.5`.
- Use the HTML scoring rule to select the preferred valid layout.

## Table Labels

Use these table meanings:

- 型号
- 产品名称 = Chinese scene name
- 包装方式 = 彩盒
- 彩盒规格(cm)
- 装箱量
- 毛重(kg)
- 净重(kg)
- 装箱规格(cm)

Do not duplicate gross/net weight in the model-name area.

## Quote Workbook Rules

When updating the user's `极客智玩.xlsx` quotation workbook:

- Preserve the existing row height, cell styles, fonts, colors, borders,
  alignment, number formats, and column widths. Populate the existing
  preformatted rows instead of rebuilding the sheet.
- Continue product codes sequentially from the user-specified starting code.
- Product name format is exactly
  `支持OEM定制-场景名 XXPCS 磁力方块磁性方块磁力积木我的世界磁性积木`.
- Unit price = `PCS * 0.38`, rounded to two decimal places.
- 包装 = `彩盒`.
- 装箱量、外箱规格、毛重、净重、包装规格 must come from
  `scripts/calculate_airplane_carton.py`.
- 备注 = `5箱起` unless the user supplies a different MOQ.
- Insert the final approved catalog-sheet PNG as a floating drawing anchored
  over the image cell. Do not paste it as cell content, a formula, or a linked
  external object.
- Before replacing the original workbook, save a backup and validate workbook
  ZIP integrity, target-row values, retained styles, drawing count, and one
  floating image anchor per populated row.

## Color Box Rules

- Color box base should be near-white with very light warm gray, not pure white if it merges into the sheet background.
- Side faces can be plain white/light gray, but box edges need subtle shadows so the package remains 3D.
- Use `approved-color-box.md` for front-face artwork, perspective, and edge QA.
- For the approved universal package, reuse the locked transparent asset rather than redrawing it for every SKU sheet.
- For a SKU-specific package, paste the exact final scene render with the same tone profile; do not regenerate it separately.
- Right top package info uses PCS, age, and cube size; catalog sheet uses `20mm`, foreign-facing box uses `0.79 IN`.
