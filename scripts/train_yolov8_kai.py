"""Real YOLOv8 training script for P0026 Kai (wildlife poaching detection).

This is a production-quality replacement for the stub in src/papers/p0026_kai_poaching/pipeline.py.

Usage:
    python scripts/train_yolov8_kai.py --config configs/p0026_kai.yaml
    python scripts/train_yolov8_kai.py --epochs 100 --batch-size 16 --data data/wildlife.yaml
"""

import argparse
import logging
import sys
from pathlib import Path

import torch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    parser = argparse.ArgumentParser(description="Train YOLOv8 for P0026 Kai (wildlife poaching detection)")
    parser.add_argument("--config", default="configs/p0026_kai.yaml", help="Path to YAML config")
    parser.add_argument("--model", default="yolov8m.pt", help="Pretrained model")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--device", default="0" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--data", default="data/wildlife/wildlife.yaml", help="Path to wildlife data YAML")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    parser.add_argument("--checkpoint", help="Resume from this checkpoint")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Training YOLOv8 for P0026 Kai (Wildlife Poaching Detection)")
    logger.info(f"  Model: {args.model}")
    logger.info(f"  Epochs: {args.epochs}")
    logger.info(f"  Batch size: {args.batch_size}")
    logger.info(f"  Image size: {args.imgsz}")
    logger.info(f"  Device: {args.device}")

    # Load config
    import yaml

    config_path = Path(args.config)
    if config_path.exists():
        with open(config_path) as f:
            yaml.safe_load(f) or {}
        logger.info(f"Loaded config from {config_path}")

    try:
        from ultralytics import YOLO
    except ImportError:
        logger.error("ultralytics not installed. Run: pip install ultralytics")
        sys.exit(1)

    # Load model
    if args.resume and args.checkpoint:
        logger.info(f"Resuming from {args.checkpoint}")
        model = YOLO(args.checkpoint)
    else:
        model = YOLO(args.model)

    # Generate wildlife data YAML if not exists
    data_yaml = Path(args.data)
    if not data_yaml.exists():
        logger.warning(f"Wildlife data YAML not found: {data_yaml}")
        logger.warning("Generating template...")
        generate_wildlife_yaml(data_yaml)

    # Train
    logger.info("Starting training...")
    results = model.train(  # noqa: F841
        data=str(data_yaml),
        epochs=args.epochs,
        batch=args.batch_size,
        imgsz=args.imgsz,
        device=args.device,
        project="models/yolov8_kai",
        name="train",
        save=True,
        save_period=10,
        patience=15,
        optimizer="AdamW",
        lr0=0.001,
        cos_lr=True,
        augment=True,
        mixup=0.1,
        copy_paste=0.1,
    )

    # Validate
    logger.info("Validating model...")
    metrics = model.val()
    logger.info(f"mAP@0.5: {metrics.box.map50:.4f}")
    logger.info(f"mAP@0.5:0.95: {metrics.box.map:.4f}")

    # Export
    export_path = Path("models/yolov8_kai/best.pt")
    if export_path.exists():
        logger.info(f"Best checkpoint saved to {export_path}")
        # Export to ONNX
        try:
            model.export(format="onnx")
            logger.info("Exported to ONNX")
        except Exception as e:
            logger.warning(f"ONNX export failed: {e}")

    # Log to MLflow
    try:
        from src.utils.mlflow_tracking import log_p0026_experiment

        log_p0026_experiment(
            map50=metrics.box.map50,
            map50_95=metrics.box.map,
            epochs=args.epochs,
            params={
                "model": args.model,
                "batch_size": args.batch_size,
                "imgsz": args.imgsz,
                "lr0": 0.001,
            },
        )
    except Exception as e:
        logger.warning(f"MLflow logging failed: {e}")

    logger.info("Training complete!")


def generate_wildlife_yaml(output_path: Path):
    """Generate YOLOv8 data YAML for wildlife poaching detection.

    Format: https://docs.ultralytics.com/datasets/detect/
    """
    template = """# Wildlife Poaching Detection Dataset
# YOLOv8 data YAML

# Train/val/test splits
train: data/wildlife/images/train
val: data/wildlife/images/val
test: data/wildlife/images/test

# Class names (modify as needed)
names:
  0: poaching_camp
  1: snares
  2: gunshots
  3: human_figure
  4: vehicle
  5: fire_痕迹
  6: wildlife_jaguar
  7: wildlife_puma
  8: wildlife_deer
  9: wildlife_peccary
  10: wildlife_tapir
  11: wildlife_macaw

# Number of classes
nc: 12
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template)
    print(f"Generated template at {output_path}")


if __name__ == "__main__":
    main()
