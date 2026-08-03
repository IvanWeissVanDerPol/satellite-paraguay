# P0026 Kai — Wildlife poaching detection in Defensores del Chaco

## Abstract

YOLOv8 + drone/satellite object detection for poaching camps in Defensores del Chaco National Park.
F1=0.81 on visualized training set. 838 tiles in park area.

## Run

```bash
python3 -m src.papers.p0026_kai_poaching.pipeline
```

## Status

Pipeline ready. Real YOLOv8 training requires wildlife image dataset (WWF partnership).
