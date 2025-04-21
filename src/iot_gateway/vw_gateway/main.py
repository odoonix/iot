#!/usr/bin/python3
from thingsboard_gateway.gateway.tb_gateway_service import TBGatewayService
from thingsboard_gateway.tb_utility.tb_loader import TBModuleLoader
import argparse
import os.path
from pyfiglet import Figlet
import pkg_resources
import typer

app = typer.Typer()


@app.command()
def main(path_cofig:str, path_extension:str):
    f = Figlet(font='big')
    print (f.renderText('Odoonix')) 
    print("Thingsboard Gateway Package Version is :" + pkg_resources.get_distribution("thingsboard-gateway").version)
    TBModuleLoader.PATHS.append(path_extension)
    TBGatewayService(path_cofig)

if __name__ == "__main__":
    app()