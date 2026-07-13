# Packaging And Formula Rules

## Cube And Box Size

- Magnetic cube size: `2cm x 2cm x 2cm`.
- Calculate color-box internal volume from cube count and a suitable airplane-box arrangement.
- Color box dimensions:
  - Length = internal length + `1cm`.
  - Width = internal width + `0.5cm`.
  - Height = internal height + `0.5cm`.
- Dimensions shown on the sheet must be outside the color box with straight dimension lines.

## Carton Quantity

Use the user's fixed rule:

- One cube weight: `0.0043kg`.
- Carton quantity must be a multiple of `12`.
- Choose the largest multiple of `12` where gross weight is `<=25kg`.
- Net weight = `pcs * carton_qty * 0.0043`.
- Gross weight = net weight + `1kg`.

If current scripts use any other maximum gross weight, update them to `25.0`.

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

## Color Box Rules

- Color box base should be near-white with very light warm gray, not pure white if it merges into the sheet background.
- Side faces can be plain white/light gray, but box edges need subtle shadows so the package remains 3D.
- Use `approved-color-box.md` for front-face artwork, perspective, and edge QA.
- For the approved universal package, reuse the locked transparent asset rather than redrawing it for every SKU sheet.
- For a SKU-specific package, paste the exact final scene render with the same tone profile; do not regenerate it separately.
- Right top package info uses PCS, age, and cube size; catalog sheet uses `20mm`, foreign-facing box uses `0.79 IN`.
