# Model Card — DINOv2

**Model:** DINOv2 (Meta AI)
**License:** Apache 2.0
**HuggingFace:** https://huggingface.co/facebook/dinov2-base
**Used in:** P0011 Yvutu (embeddings) + P0010 Tava-i (multi-modal)

## Model details

- **Architecture:** Vision Transformer (ViT)
- **Size:** 86M (base) to 1.1B (giant)
- **Input:** 224x224 RGB images (16-band variant available)
- **Output:** 768-dim embeddings
- **Pre-training:** Self-supervised (DINO + iBOT)

## Intended use

- Self-supervised vision features
- Transfer learning for downstream tasks
- Image classification, segmentation, retrieval
- Multi-modal (text + image) when combined with CLIP

## Training data

- LVD-142M (142M curated images)
- Self-distillation framework
- Multi-crop + multi-scale

## Evaluation

- **ImageNet:** 84.5% top-1 (DINOv2-g)
- **Image segmentation:** Strong performance
- **Depth estimation:** Competitive
- **Retrieval:** Strong zero-shot

## Limitations

- Trained primarily on natural images
- May need fine-tuning for satellite/aerial imagery
- 224x224 input size limits spatial context
- Vision-only (no language)

## Ethical considerations

- Used for: classification, retrieval, segmentation
- Should not be used for: surveillance without consent, biometric identification

## Citation

```bibtex
@misc{oquab2024dinov2,
  title={DINOv2: Learning Robust Visual Features without Supervision},
  author={Oquab, Maxime and Darcet, Timothée and Moutakanni, Theo and Vo, Huy and Szafraniec, Marc and Khalidov, Vasil and Fernandez, Pierre and Haziza, Daniel and Massa, Luca and El-Nouby, Alaaeldin and others},
  year={2024},
  archiveprefix={arXiv},
  eprint={2304.07193}
}
```
