#!/bin/bash
cd venv/bin
source activate
cd ../..
python vw-gateway/main.py --config configs/conf.yaml --extension extensions
