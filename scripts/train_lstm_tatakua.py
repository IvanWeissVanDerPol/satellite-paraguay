"""Real LSTM training script for P0035 Tatakua (Asunción PM2.5 forecasting).

Usage:
    python scripts/train_lstm_tatakua.py --config configs/p0035_tatakua.yaml --epochs 50
"""
import argparse
import logging
from pathlib import Path
import sys
import time

import numpy as np
import pandas as pd
import torch

sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    parser = argparse.ArgumentParser(description="Train LSTM for P0035 Tatakua (PM2.5 forecasting)")
    parser.add_argument("--config", default="configs/p0035_tatakua.yaml")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--n-layers", type=int, default=2)
    parser.add_argument("--horizon", type=int, default=7)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Training LSTM for P0035 Tatakua (Asunción PM2.5)")

    # Load data
    from src.external import (
        fetch_openaq_asuncion,
        fetch_sentinel5p_no2,
        fetch_sentinel5p_o3,
    )
    from src.utils import set_seed

    set_seed(42)

    logger.info("Loading OpenAQ data...")
    openaq = fetch_openaq_asuncion(days=730, parameter="pm25")  # 2 years
    if openaq.empty or "value" not in openaq.columns:
        logger.warning("OpenAQ empty; using synthetic")
        from src.external.openaq_client import generate_synthetic_openaq_for_station
        openaq = generate_synthetic_openaq_for_station(-25.26, -57.58, "pm25")

    # Aggregate to monthly
    openaq["date_utc"] = pd.to_datetime(openaq["date_utc"], errors="coerce")
    openaq = openaq.dropna(subset=["date_utc"])
    openaq["year_month"] = openaq["date_utc"].dt.to_period("M").astype(str)
    monthly_pm25 = openaq.groupby("year_month")["value"].mean().reset_index()
    monthly_pm25.columns = ["year_month", "pm25"]

    # Add Sentinel-5P features
    bbox = {"min_lon": -57.7, "max_lon": -57.4, "min_lat": -25.4, "max_lat": -25.2}
    no2_data = fetch_sentinel5p_no2(bbox, "2023-01-01", "2025-12-31")
    o3_data = fetch_sentinel5p_o3(bbox, "2023-01-01", "2025-12-31")

    # Match by year-month
    def get_month(s5p_dict, ym):
        for k, v in s5p_dict.items():
            if k.startswith(ym):
                return v
        return 0.0

    monthly_pm25["no2"] = monthly_pm25["year_month"].apply(lambda ym: get_month(no2_data, ym))
    monthly_pm25["o3"] = monthly_pm25["year_month"].apply(lambda ym: get_month(o3_data, ym))
    monthly_pm25 = monthly_pm25.sort_values("year_month").reset_index(drop=True)

    logger.info(f"Monthly records: {len(monthly_pm25)}")
    logger.info(f"  Mean PM2.5: {monthly_pm25['pm25'].mean():.1f} µg/m³")

    # Build time-series dataset
    feature_cols = ["pm25", "no2", "o3"]
    values = monthly_pm25[feature_cols].values

    # Normalize
    mean = values.mean(axis=0)
    std = values.std(axis=0) + 1e-8
    values_norm = (values - mean) / std

    # Build sequences
    sequence_length = 6  # 6 months input
    X, y = [], []
    for i in range(len(values_norm) - sequence_length - args.horizon + 1):
        X.append(values_norm[i:i + sequence_length])
        y.append(values_norm[i + sequence_length:i + sequence_length + args.horizon, 0])  # PM2.5 only

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)
    logger.info(f"Training samples: {X.shape}, target horizon: {args.horizon}")

    if len(X) == 0:
        logger.error("Not enough data to train")
        return

    # Train/val split
    split = int(0.8 * len(X))
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]

    # LSTM model
    class LSTMForecaster(torch.nn.Module):
        def __init__(self, input_dim, hidden_dim, n_layers, horizon):
            super().__init__()
            self.lstm = torch.nn.LSTM(
                input_dim, hidden_dim, n_layers,
                batch_first=True, dropout=0.2 if n_layers > 1 else 0,
            )
            self.fc = torch.nn.Linear(hidden_dim, horizon)

        def forward(self, x):
            lstm_out, _ = self.lstm(x)
            return self.fc(lstm_out[:, -1, :])

    model = LSTMForecaster(
        input_dim=len(feature_cols),
        hidden_dim=args.hidden_dim,
        n_layers=args.n_layers,
        horizon=args.horizon,
    ).to(args.device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    criterion = torch.nn.MSELoss()

    # Convert to tensors
    X_train_t = torch.from_numpy(X_train).to(args.device)
    y_train_t = torch.from_numpy(y_train).to(args.device)
    X_val_t = torch.from_numpy(X_val).to(args.device)
    y_val_t = torch.from_numpy(y_val).to(args.device)

    # Training loop
    best_val_mae = float("inf")
    checkpoint_dir = Path("models/lstm_tatakua")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    for epoch in range(args.epochs):
        model.train()
        total_loss = 0.0
        n_batches = 0

        # Mini-batch training
        for i in range(0, len(X_train_t), args.batch_size):
            batch_X = X_train_t[i:i + args.batch_size]
            batch_y = y_train_t[i:i + args.batch_size]

            optimizer.zero_grad()
            pred = model(batch_X)
            loss = criterion(pred, batch_y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            n_batches += 1

        scheduler.step()
        avg_loss = total_loss / max(1, n_batches)

        # Validation
        model.eval()
        with torch.no_grad():
            val_pred = model(X_val_t)
            val_pred_unnorm = val_pred.cpu().numpy() * std[0] + mean[0]
            val_y_unnorm = y_val_t.cpu().numpy() * std[0] + mean[0]
            val_mae = float(np.mean(np.abs(val_pred_unnorm - val_y_unnorm)))

        logger.info(
            f"Epoch {epoch+1}/{args.epochs} | "
            f"Train Loss: {avg_loss:.4f} | "
            f"Val MAE: {val_mae:.2f} µg/m³"
        )

        # Save best
        if val_mae < best_val_mae:
            best_val_mae = val_mae
            torch.save({
                "model_state_dict": model.state_dict(),
                "epoch": epoch,
                "best_val_mae": best_val_mae,
                "mean": mean.tolist(),
                "std": std.tolist(),
            }, checkpoint_dir / "best.pt")

    # Final
    final_path = checkpoint_dir / "final.pt"
    torch.save(model.state_dict(), final_path)
    logger.info(f"Training complete. Final MAE: {best_val_mae:.2f} µg/m³")
    logger.info(f"Best model: {checkpoint_dir}/best.pt")

    # MLflow logging
    try:
        from src.utils.mlflow_tracking import log_p0035_experiment
        log_p0035_experiment(
            val_mae=best_val_mae,
            epochs=args.epochs,
            params={
                "lr": args.lr,
                "hidden_dim": args.hidden_dim,
                "n_layers": args.n_layers,
                "horizon": args.horizon,
            },
        )
    except Exception as e:
        logger.warning(f"MLflow logging failed: {e}")


if __name__ == "__main__":
    main()
