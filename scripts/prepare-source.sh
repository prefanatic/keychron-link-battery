#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$project_dir/.build/source"
revision=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["revision"])' "$project_dir/firmware/manifest.json")
repository=${QMK_REPOSITORY:-https://github.com/Keychron/qmk_firmware.git}

if [ -e "$source_dir" ]; then
    echo 'The source directory already exists. Use scripts/build.sh or a fresh checkout.' >&2
    exit 1
fi
mkdir -p "$project_dir/.build"
git clone --no-checkout "$repository" "$source_dir"
git -C "$source_dir" checkout --detach "$revision"
git -C "$source_dir" submodule update --init --depth 1 lib/chibios lib/chibios-contrib lib/printf
git -C "$source_dir" apply --check "$project_dir/firmware/v1-max-battery.patch"
git -C "$source_dir" apply "$project_dir/firmware/v1-max-battery.patch"
