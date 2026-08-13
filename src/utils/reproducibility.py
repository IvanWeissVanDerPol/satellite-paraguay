"""Reproducibility utilities.

Set random seeds + capture environment for all experiments.
"""

import json
import os
import platform
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Random seeds
DEFAULT_SEED = 42


def set_seed(seed: int = DEFAULT_SEED) -> None:
    """Set random seed for all libraries.

    Args:
        seed: integer to seed all RNGs
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
        # For deterministic CUDA operations
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

    try:
        import tensorflow as tf

        tf.random.set_seed(seed)
    except ImportError:
        pass


def get_git_hash() -> Optional[str]:
    """Get current git commit hash."""
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=Path(__file__).parent.parent,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_git_branch() -> Optional[str]:
    """Get current git branch."""
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=Path(__file__).parent.parent,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_python_version() -> str:
    """Get Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_system_info() -> Dict:
    """Get comprehensive system info."""
    info = {
        "python_version": get_python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "system": platform.system(),
        "release": platform.release(),
    }

    try:
        import torch

        info["cuda_available"] = torch.cuda.is_available()  # type: ignore[assignment]
        if torch.cuda.is_available():
            info["cuda_version"] = torch.version.cuda  # type: ignore[assignment]
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_count"] = torch.cuda.device_count()  # type: ignore[assignment]
            info["gpu_memory_gb"] = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # type: ignore[assignment]  # noqa: E501
        else:
            info["cuda_available"] = False  # type: ignore[assignment]
    except ImportError:
        info["cuda_available"] = False  # type: ignore[assignment]

    try:
        import psutil

        info["cpu_count"] = psutil.cpu_count()
        info["ram_gb"] = psutil.virtual_memory().total / (1024**3)
    except ImportError:
        pass

    info["git_hash"] = get_git_hash()  # type: ignore[assignment]
    info["git_branch"] = get_git_branch()  # type: ignore[assignment]
    info["timestamp"] = datetime.now().isoformat()
    info["cwd"] = str(Path.cwd())

    return info


def capture_environment(output_path: Path) -> Dict:
    """Capture full environment info and save to JSON.

    Args:
        output_path: where to save the JSON

    Returns:
        Dict with all environment info
    """
    info = get_system_info()

    # Add installed packages
    try:
        import pkg_resources

        info["packages"] = {d.project_name: d.version for d in pkg_resources.working_set}
    except Exception:
        pass

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(info, indent=2, default=str))

    return info


def verify_reproducibility(
    operation,
    expected_output,
    tolerance: float = 1e-5,
    n_runs: int = 3,
) -> bool:
    """Verify an operation is reproducible.

    Runs the operation multiple times and checks output consistency.
    """
    outputs = []
    for i in range(n_runs):
        set_seed(DEFAULT_SEED + i)
        out = operation()
        outputs.append(out)

    # Check all outputs are close
    for out in outputs[1:]:
        try:
            import numpy as np

            if not np.allclose(out, outputs[0], atol=tolerance):
                return False
        except Exception:
            if out != outputs[0]:
                return False

    return True


if __name__ == "__main__":
    print("Reproducibility utilities")
    print("=" * 60)

    # Test set_seed
    set_seed(42)
    import numpy as np

    print(f"np.random.rand(3) after seed 42: {np.random.rand(3)}")

    set_seed(42)
    print(f"np.random.rand(3) after seed 42 again: {np.random.rand(3)} (should be same)")

    # Test environment capture
    print("\nSystem info:")
    info = get_system_info()
    for k, v in info.items():
        print(f"  {k}: {v}")

    # Save to file
    output_path = Path("logs/environment.json")
    capture_environment(output_path)
    print(f"\nSaved to {output_path}")
