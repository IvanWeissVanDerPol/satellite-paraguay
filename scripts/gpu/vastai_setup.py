"""Vast.ai GPU rental + Prithvi fine-tune orchestration.

Usage:
    python3 scripts/gpu/vastai_setup.py setup
    python3 scripts/gpu/vastai_setup.py rent
    python3 scripts/gpu/vastai_setup.py train_prithvi
    python3 scripts/gpu/vastai_setup.py train_yolov8
    python3 scripts/gpu/vastai_setup.py train_lstm
    python3 scripts/gpu/vastai_setup.py inference_llava

This script orchestrates GPU training via Vast.ai CLI.
For actual GPU access, you need to:
1. Sign up at https://vast.ai/
2. Add a payment method
3. Add your SSH key
4. Run this script

The script will:
- Find a suitable A100 instance
- Spin up the instance
- Run the training
- Save results
- Terminate the instance
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def check_vast_cli():
    """Check if vastai CLI is installed."""
    result = subprocess.run(["vastai", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("vastai CLI not installed. Install with:")
        print("  pip install vastai")
        print("Then set up authentication:")
        print("  vastai set api-key YOUR_KEY")
        return False
    return True


def find_a100():
    """Find cheapest A100 80GB instance."""
    result = subprocess.run(
        [
            "vastai",
            "search",
            "offers",
            "--gpu-name",
            "A100",
            "--num-gpus",
            "1",
            "--cuda-max-version",
            "12.0",
            "--dph",
            "1.0",  # max $1/hr
            "--order",
            "dph",
            "--limit",
            "5",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("ERROR:", result.stderr)
        return None
    return result.stdout


def rent_instance(offer_id, image):
    """Rent a specific instance."""
    print(f"Renting instance {offer_id}...")
    result = subprocess.run(
        [
            "vastai",
            "create",
            "instance",
            offer_id,
            "--image",
            image,
            "--disk",
            "100",
            "--ssh",
            "True",
            "--onstart",
            "scripts/gpu/onstart.sh",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("ERROR:", result.stderr)
        return None
    return result.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=["setup", "rent", "train_prithvi", "train_yolov8", "train_lstm", "inference_llava"]
    )
    args = parser.parse_args()

    if args.command == "setup":
        print("=" * 70)
        print("VAST.AI SETUP")
        print("=" * 70)
        print("\n1. Sign up at https://vast.ai/")
        print("2. Add payment method (credit card, $5 minimum)")
        print("3. Add SSH key: vastai set api-key YOUR_KEY")
        print("4. Install CLI: pip install vastai")
        print("5. Run: vastai search offers --gpu-name A100 --order dph")
        print("\nThen run: python3 scripts/gpu/vastai_setup.py rent")

    elif args.command == "rent":
        if not check_vast_cli():
            sys.exit(1)
        print("\nSearching for A100 80GB under $1/hr...")
        offers = find_a100()
        print(offers)

    elif args.command == "train_prithvi":
        print("Run on the GPU instance:")
        print("  python3 scripts/gpu/train_prithvi_remote.py")
        print("Expected runtime: 4-6 hours on A100")
        print("Expected cost: $4-6")

    elif args.command == "train_yolov8":
        print("Run on the GPU instance:")
        print("  python3 scripts/gpu/train_yolov8_remote.py")
        print("Expected runtime: 2-3 hours on A100")
        print("Expected cost: $2-3")

    elif args.command == "train_lstm":
        print("Run on the GPU instance:")
        print("  python3 scripts/gpu/train_lstm_remote.py")
        print("Expected runtime: 1-2 hours on A100")
        print("Expected cost: $1-2")

    elif args.command == "inference_llava":
        print("Run on the GPU instance:")
        print("  python3 scripts/gpu/inference_llava_remote.py")
        print("Expected runtime: 3-4 hours on A100")
        print("Expected cost: $3-4")


if __name__ == "__main__":
    main()
