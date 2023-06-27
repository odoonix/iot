#!/bin/bash
VW_HOME=/root
VW_GATEWAY_HOME=/root/git/odoo-iot/vw-gateway
cd "${VW_GATEWAY_HOME}"
/usr/bin/python3 \
  "${VW_GATEWAY_HOME}/main.py" \
  --config "${VW_HOME}/.vw-gateway/conf.yaml" \
  --extension "${VW_GATEWAY_HOME}/extensions"
