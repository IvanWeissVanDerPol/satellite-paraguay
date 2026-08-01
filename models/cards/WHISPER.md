# Model Card — Whisper

**Model:** Whisper (OpenAI)
**License:** MIT
**HuggingFace:** https://huggingface.co/openai/whisper-large-v3
**Used in:** P0015 Sy (clinical scribe, related project)

## Model details

- **Architecture:** Encoder-decoder transformer
- **Size:** 39M (tiny) to 1.5B (large-v3)
- **Input:** 30-second audio chunks (16kHz)
- **Output:** Text transcription (multilingual)
- **Pre-training:** 680K hours labeled + 4M hours pseudo-labeled

## Intended use

- Speech-to-text transcription
- Multilingual (99 languages including Spanish + Guaraní support)
- Translation (English → other languages)

## Training data

- **Pre-training:** Diverse audio from internet
- **Multilingual:** Strong for European languages, weaker for low-resource
- **Spanish:** Strong (3rd most spoken language)
- **Guaraní:** Limited support

## Evaluation

- **English WER:** 2.7% (large-v3)
- **Spanish WER:** 2.8% (large-v3)
- **Code-switching:** Struggles (single-language pretraining)
- **Noisy audio:** Robust

## Limitations

- Hallucinates on silent audio
- Struggles with heavy accents
- Code-switching (Spanish-Guaraní jopara) under-tested
- Limited Guaraní support

## Ethical considerations

- Used for: accessibility, transcription, clinical notes
- Should not be used for: surveillance without consent
- Hallucinations can be dangerous in clinical settings
- CARE Principles for indigenous language applications

## Why Whisper for P0015?

- **Multilingual:** supports Spanish natively
- **Open-source:** no API costs
- **Clinical-grade:** 2.7% WER is good enough for medical notes

## Citation

```bibtex
@misc{whisper2022,
  title={Robust Speech Recognition via Large-Scale Weak Supervision},
  author={Radford, Alec and Kim, Jong Wook and Xu, Tao and Brockman, Greg and McLeavey, Christine and Sutskever, Ilya},
  year={2022},
  archiveprefix={arXiv},
  eprint={2212.04356}
}
```
