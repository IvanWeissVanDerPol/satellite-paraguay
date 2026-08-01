# Model Card — YOLOv8

**Model:** YOLOv8 (Ultralytics)
**License:** GPL-3.0 (commercial use requires license)
**GitHub:** https://github.com/ultralytics/ultralytics
**Used in:** P0026 Kai (wildlife poaching detection)

## Model details

- **Architecture:** CSPDarknet + PANet + YOLO head
- **Variants:** n, s, m, l, x (nano to extra-large)
- **Size:** 3M to 68M parameters
- **Input:** 640x640 RGB images
- **Output:** Bounding boxes + class probabilities
- **Pre-training:** COCO dataset (80 classes)

## Intended use

- Real-time object detection
- Edge deployment (Jetson, Raspberry Pi)
- Wildlife detection (transfer learning)
- Poaching camp detection

## Training data

- **COCO:** 80 classes, 1.5M images
- **iNaturalist:** 1M images, 10K species
- **Roboflow Universe:** custom datasets (for fine-tuning)

## Evaluation

- **COCO benchmark:**
  - YOLOv8m: 50.2 mAP@0.5:0.95
  - YOLOv8l: 52.9 mAP@0.5:0.95
- **Speed:** YOLOv8n: 1.2ms @ 640px (V100 GPU)
- **Transfer learning:** strong performance on wildlife data with 1K-5K labeled images

## Limitations

- Pre-trained on English-language COCO (Spanish/Guaraní labels need translation)
- Wildlife classes need custom training data
- Heavy occlusion in dense forest may reduce recall
- Domain shift (satellite → drone) requires adaptation

## Ethical considerations

- Privacy concerns when detecting in urban areas
- Wildlife data should be reviewed by conservationists
- Misclassification could lead to false poaching accusations
- Should be deployed with human-in-the-loop

## Citation

```bibtex
@software{yolov8,
  title={Ultralytics YOLOv8},
  author={Jocher, Glenn and Chaurasia, Ayush and Qiu, Jing},
  year={2023},
  url={https://github.com/ultralytics/ultralytics}
}
```
