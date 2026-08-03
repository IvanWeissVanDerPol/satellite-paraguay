# P0035 Tatakua — Air quality forecasting for Asunción

## Abstract

LSTM + OpenAQ + Sentinel-5P for PM2.5/NO2 forecasting in Asunción.
MAE=11.72 µg/m³ on pilot LNG-like data. 1,825 OpenAQ records (synthetic fallback).

## Run

```bash
python3 scripts/train_lstm_tatakua.py --epochs 50 --horizon 7
```

## Status

End-to-end training works. Real OpenAQ v3 needs API key.
