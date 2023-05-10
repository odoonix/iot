#!/usr/bin/python3
from thingsboard_gateway.gateway.tb_gateway_service import TBGatewayService
from thingsboard_gateway.tb_utility.tb_loader import TBModuleLoader

TBModuleLoader.PATHS.append("./extensions")

TBGatewayService("./tb_gateway.yaml")