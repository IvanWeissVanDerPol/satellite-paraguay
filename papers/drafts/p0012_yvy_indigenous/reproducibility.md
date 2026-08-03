# P0012 Yvy — Reproducibility

## 1. Data

```
Source: /root/paraguay-geodata/exports/web/data/
Files:
  - admin/catastro_paraguay.geojson (8,010 parcels)
  - indigenous_territories.geojson (10 territories)
  - tile_index.json (7,912 tiles)
```

## 2. Code

```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay
cd satellite-paraguay
pip install -r requirements.txt

# Run conflict detection
python3 -c "
import sys
sys.path.insert(0, '.')
from src.paraguay_admin.real_analysis import detect_conflicts_real
result = detect_conflicts_real(buffer_m=100)
print(f'Conflicts: {result[\"conflict_parcels\"]} / {result[\"total_parcels\"]}')
"
```

## 3. LLaVA Inference

```python
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
from PIL import Image
import torch

processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
model = LlavaNextForConditionalGeneration.from_pretrained(
    "llava-hf/llava-v1.6-mistral-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)

image = Image.open("satellite_tile.png")
prompt = "USER: <image>\nDescribe the land use visible. Any signs of indigenous land use? Estimate conflict severity. ASSISTANT:"

inputs = processor(prompt, image, return_tensors="pt").to("cuda")
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True))
```

## 4. CARE Principles Compliance

- [x] Code released under MIT license
- [ ] Community consent obtained (TBD — partnership with INDI required)
- [ ] Findings shared with communities before publication (TBD)
- [ ] Opt-out mechanism available
- [ ] Error correction channels provided

## 5. Hardware

- Conflict detection: 1 GB RAM, 5 seconds
- LLaVA inference: 16 GB GPU + 32 GB RAM, 30 seconds per tile
- Recommended: Vast.ai A100 ($1/hr)
