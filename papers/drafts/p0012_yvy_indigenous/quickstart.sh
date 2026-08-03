#!/usr/bin/env bash
# P0012 Yvy quickstart
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../../.."
python3 -c "
import sys
sys.path.insert(0, '.')
from src.paraguay_admin.real_analysis import detect_conflicts_real
result = detect_conflicts_real(buffer_m=100)
print(f'Conflicts: {result[\"conflict_parcels\"]} of {result[\"total_parcels\"]} parcels')
print(f'Conflict fraction: {result[\"conflict_fraction\"]*100:.2f}%')
print(f'Buffer: {result[\"buffer_m\"]}m')
print(f'Indigenous territories: {result[\"total_indigenous_territories\"]}')
print(f'Output columns: {list(result[\"conflicts\"].columns)}')
print(f'Sample conflict:')
print(result['conflicts'].head(1).to_string())
"
