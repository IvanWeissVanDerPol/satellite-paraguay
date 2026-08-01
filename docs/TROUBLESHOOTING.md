# Troubleshooting Guide

Common errors and solutions for SatelliteCV-Paraguay.

## Installation issues

### `pip install -r requirements.txt` fails

**Symptom:** `ERROR: Could not build wheels for ...`

**Solutions:**

1. **Update pip:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

2. **Install build tools:**
   ```bash
   # Ubuntu/Debian
   sudo apt install build-essential python3-dev

   # macOS
   xcode-select --install
   ```

3. **Use conda (alternative):**
   ```bash
   conda install --file requirements.txt
   ```

### `gdal` import error

**Symptom:** `ImportError: No module named 'gdal'` or similar

**Solutions:**

1. **Install gdal system-wide:**
   ```bash
   # Ubuntu/Debian
   sudo apt install gdal-bin libgdal-dev

   # macOS
   brew install gdal
   ```

2. **Use conda:**
   ```bash
   conda install -c conda-forge gdal
   ```

3. **Use rasterio:**
   ```bash
   pip install rasterio  # already includes gdal
   ```

### `torch` CUDA mismatch

**Symptom:** `RuntimeError: CUDA unavailable` or version mismatch

**Solutions:**

1. **Reinstall PyTorch with correct CUDA:**
   ```bash
   # CUDA 11.8
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

   # CUDA 12.1
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

   # CPU only
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

2. **Check CUDA version:**
   ```bash
   nvcc --version
   nvidia-smi
   ```

## Data loading issues

### `/root/paraguay-geodata/` not found

**Symptom:** `FileNotFoundError: /root/paraguay-geodata/exports/web/data/...`

**Solutions:**

1. **Check if path exists:**
   ```bash
   ls /root/paraguay-geodata/exports/web/data/
   ```

2. **Mount from different path:**
   ```bash
   # If data is in different location
   sudo ln -s /path/to/data /root/paraguay-geodata
   ```

3. **Download fresh data:**
   ```bash
   # TODO: add download script
   ```

### `tile_index.json` parsing fails

**Symptom:** JSON decode error

**Solution:** Check if file is valid JSON:
```bash
python -c "import json; print(json.load(open('/root/paraguay-geodata/exports/web/data/tile_index.json'))['total_tiles'])"
```

## Google Earth Engine issues

### `ee.Initialize()` fails

**Symptom:** `Please run earthengine authenticate`

**Solution:**
```bash
earthengine authenticate
```

This opens a browser for OAuth flow. After authentication, try again.

### `ee.Asset` not found

**Symptom:** `Asset not found`

**Solution:** Verify asset name is correct:
```python
import ee
ee.Initialize()
print(ee.data.getAssetList('projects/ee-yourname/assets/'))
```

## Model training issues

### GPU out of memory

**Symptom:** `RuntimeError: CUDA out of memory. Tried to allocate X GB`

**Solutions:**

1. **Reduce batch size:**
   ```python
   # Was: batch_size=32
   # Try: batch_size=8
   ```

2. **Use gradient accumulation:**
   ```python
   accumulation_steps = 4
   for i in range(0, len(data), batch_size):
       loss = model(batch)
       loss.backward()
       if (i // batch_size) % accumulation_steps == 0:
           optimizer.step()
           optimizer.zero_grad()
   ```

3. **Use mixed precision (fp16):**
   ```python
   from torch.cuda.amp import autocast, GradScaler
   scaler = GradScaler()
   with autocast():
       loss = model(batch)
   scaler.scale(loss).backward()
   scaler.step(optimizer)
   scaler.update()
   ```

4. **Use smaller model:**
   - Prithvi-100M instead of 300M
   - LLaVA-1.6-7B instead of 34B
   - YOLOv8n instead of YOLOv8l

5. **Use Cloud GPU with more VRAM:**
   - Vast.ai / RunPod with A100 (80 GB)

### Training is slow

**Solutions:**

1. **Use mixed precision** (as above)
2. **Increase batch size** (if GPU has memory)
3. **Use larger learning rate** with warmup
4. **Use compile (PyTorch 2.0+):**
   ```python
   model = torch.compile(model)
   ```
5. **Use multi-GPU:**
   ```python
   model = torch.nn.DataParallel(model)
   ```

### Model not converging

**Solutions:**

1. **Lower learning rate:** `lr=0.0001` instead of `0.001`
2. **Add warmup:** `warmup_steps=100`
3. **Use cosine schedule:** `scheduler = CosineAnnealingLR`
4. **Increase epochs**
5. **Try different optimizer:** `AdamW` instead of `SGD`
6. **Check data quality:** verify labels are correct
7. **Use pretrained model:** don't train from scratch

## Dashboard issues

### Dashboard not loading

**Symptom:** Blank page at localhost:8501

**Solutions:**

1. **Check port:** `lsof -i :8501`
2. **Try different port:**
   ```bash
   streamlit run dashboard/app.py --server.port=8502
   ```
3. **Check logs:**
   ```bash
   streamlit run dashboard/app.py --logger.level=debug
   ```

### Data not showing in dashboard

**Solutions:**

1. **Verify data files exist**
2. **Check paths in dashboard/app.py**
3. **Check data format** (GeoJSON, not CSV, etc.)

## API issues

### `uvicorn` not found

**Solution:**
```bash
pip install uvicorn fastapi pydantic
```

### API returns 500

**Solutions:**

1. **Check logs** in `logs/api.log`
2. **Test endpoint directly:**
   ```bash
   curl http://localhost:8000/health
   ```
3. **Check OpenAPI docs:** http://localhost:8000/docs

### API slow

**Solutions:**

1. **Add caching** (Redis)
2. **Use async endpoints**
3. **Batch predictions**
4. **Use smaller model variants**

## Performance issues

### Sentinel-2 download is slow

**Solutions:**

1. **Use Google Earth Engine** (faster than Copernicus Hub)
2. **Use multiple parallel downloads:**
   ```python
   from concurrent.futures import ThreadPoolExecutor
   with ThreadPoolExecutor(max_workers=8) as ex:
       ex.map(download_tile, tile_list)
   ```
3. **Cache tiles locally**

### Embeddings take forever

**Solutions:**

1. **Use mixed precision**
2. **Use smaller batch size if OOM, larger if not**
3. **Cache embeddings after first compute**
4. **Use DINOv2 (faster than Prithvi)**

## Versioning issues

### Conflicts with system Python

**Solutions:**

1. **Use pyenv:**
   ```bash
   pyenv install 3.10
   pyenv global 3.10
   ```

2. **Use conda:**
   ```bash
   conda create -n satellite python=3.10
   conda activate satellite
   ```

3. **Use docker:**
   ```bash
   docker run -it satellite-paraguay:latest bash
   ```

## Debugging tips

### Use the Python debugger

```python
import pdb; pdb.set_trace()
```

### Use logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use `rich` for better tracebacks

```bash
pip install rich
python -m rich.traceback myscript.py
```

### Use `py-spy` for profiling

```bash
pip install py-spy
py-spy dump --pid 12345
```

## Getting help

1. Check `docs/FAQ.md`
2. Search GitHub Issues
3. Email advisor
4. Post on Discord/Slack (if available)

## Common error messages

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'X'` | `pip install X` |
| `FileNotFoundError: [Errno 2]` | Check file path |
| `PermissionError: [Errno 13]` | `chmod +x file` or use sudo |
| `ConnectionError: HTTPSConnectionPool` | Check internet connection |
| `MemoryError` | Use smaller batch size |
| `RuntimeError: CUDA out of memory` | Use smaller batch + mixed precision |
| `KeyError: 'X'` | Check data file has key 'X' |
| `JSONDecodeError` | Validate JSON file |
