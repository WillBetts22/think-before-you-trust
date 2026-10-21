#!/bin/bash
# Fetches MuSiQue v1.0 (https://github.com/stonybrooknlp/musique) into this folder.
# Mirrors the official download_data.sh. If gdown fails with "too many users",
# Google Drive's quota is exhausted; retry later or download the zip manually from
# https://drive.google.com/file/d/1tGdADlNjWFaHLeZZGShh2IRcpO6Lv24h/view
# and unzip it here.

set -e
cd "$(dirname "$0")"

ZIP_NAME="musique_v1.0.zip"
gdown 1tGdADlNjWFaHLeZZGShh2IRcpO6Lv24h -O "$ZIP_NAME"
unzip -o "$ZIP_NAME"
rm "$ZIP_NAME"
rm -rf __MACOSX
