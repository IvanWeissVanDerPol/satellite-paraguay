# Model Card — LLaVA-1.6

**Model:** LLaVA-1.6 (Large Language and Vision Assistant)
**License:** Apache 2.0 (commercial-friendly)
**HuggingFace:** https://huggingface.co/llava-hf
**Used in:** P0012 Yvy (indigenous territory mapping)

## Model details

- **Architecture:** LLaMA + CLIP ViT + projection layer
- **Size:** 7B, 13B, 34B, 65B parameters
- **Input:** Image + text prompt
- **Output:** Text response
- **Pre-training:** LLaVA-Instruct-150K + LLaVA-1.5-Instruct

## Intended use

- Visual question answering
- Image captioning
- Open-vocabulary recognition
- Document understanding
- Native-language place name recognition

## Training data

- **LLaVA-Pretrain:** 595K image-caption pairs
- **LLaVA-Instruct:** 150K instruction-following examples
- **LLaVA-1.5 mix:** COCO, VisualGenome, ShareGPT4V

## Evaluation

- **VQA v2:** 80.0% (LLaVA-1.5-13B)
- **MM-Bench:** 67.4
- **MMBench-CN:** Chinese benchmark
- **Native language support:** limited for Spanish/Guaraní

## Limitations

- Trained primarily on English + Chinese
- Spanish support exists but limited Guaraní support
- Hallucinates facts (e.g., place names may be wrong)
- Should not be used for legal/critical decisions without verification

## Ethical considerations

- Privacy: should not identify individuals
- Bias: may perpetuate Western stereotypes
- Indigenous place names should be verified with community
- Should not be used to override community knowledge

## Why LLaVA-1.6 instead of GPT-4V?

- **Cost:** LLaVA-1.6 is free, GPT-4V costs $0.03/image
- **Privacy:** LLaVA can run locally, GPT-4V sends to OpenAI
- **Reproducibility:** LLaVA outputs are deterministic, GPT-4V can vary
- **Indigenous data sovereignty:** local deployment preferred for CARE Principles

## Citation

```bibtex
@inproceedings{liu2024llavanext,
  title={LLaVA-NeXT: Improved reasoning, OCR, and world knowledge},
  author={Liu, Haotian and Li, Chunyuan and Li, Yuheng and Lee, Yong Jae},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  year={2024}
}
```
