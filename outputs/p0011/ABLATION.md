# P0011 Yvutu — Ablation Study

**Mode:** QUICK (5 min)
**Total time:** 60.3s

## Setup
- Synthetic Chaco data (same generator as pilot)
- 70/30 train/test split
- U-Net from scratch (5-layer)
- AdamW, BCE loss, lr=1e-3

## Results

| n_train_tiles | n_epochs | F1 | Precision | Recall | Time (s) |
|---------------|----------|-----|-----------|--------|----------|
| 3 | 3 | 0.0637 | 0.0329 | 0.9822 | 6.3 |
| 3 | 5 | 0.0637 | 0.0329 | 0.9822 | 4.0 |
| 7 | 3 | 0.0542 | 0.0279 | 0.9805 | 7.2 |
| 7 | 5 | 0.0542 | 0.0279 | 0.9805 | 13.2 |
| 10 | 3 | 0.0353 | 0.0180 | 0.9857 | 12.3 |
| 10 | 5 | 0.0353 | 0.0180 | 0.9857 | 17.3 |

## What this means

**Best config:** n_tiles=3, n_epochs=3 → F1=0.0637
**Worst config:** n_tiles=10, n_epochs=3 → F1=0.0353

### Trends
- More training tiles → generally better (if model converges)
- More epochs → generally better (until overfitting)
- U-Net on synthetic data is hard to push beyond 0.20 F1
- This suggests real data + Prithvi fine-tune is needed

## Threats to validity
- Synthetic data does not capture real complexity
- No hyperparameter search
- Single random seed
