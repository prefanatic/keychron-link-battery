#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$project_dir/.build/source"
python3 "$project_dir/scripts/check.py" --source "$source_dir"
for tool in arm-none-eabi-gcc dfu-suffix make; do
    command -v "$tool" >/dev/null || { echo "Required tool is absent: $tool" >&2; exit 1; }
done
target=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["target"])' "$project_dir/firmware/manifest.json")
make -C "$source_dir" "$target"
cp "$source_dir/keychron_v1_max_ansi_encoder_keychron.bin" "$project_dir/.build/v1-max-ansi-battery-experimental.bin"
python3 "$project_dir/scripts/check.py"
