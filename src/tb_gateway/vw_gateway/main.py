#!/usr/bin/python3
from thingsboard_gateway.gateway.tb_gateway_service import TBGatewayService
from thingsboard_gateway.tb_utility.tb_loader import TBModuleLoader
import os.path
from pyfiglet import Figlet
import pkg_resources
import typer
import signal
import sys
import logging
import shutil
from pathlib import Path
import importlib.resources as resources
import tb_gateway.vw_gateway.templates as templates

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = typer.Typer()


gateway = None


def signal_handler(sig, frame):
    log.info("Received SIGINT, stopping the gateway...")
    global gateway
    if gateway is not None:
        try:
            gateway.stop()
            log.info("Gateway stopped successfully.")
        except Exception as e:
            log.error(f"Error stopping gateway: {e}")
    else:
        log.warning("Gateway instance not initialized.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


@app.command()
def main(path_cofig: str, path_extension: str):
    f = Figlet(font='big')
    print(f.renderText('Odoonix'))
    print("Thingsboard Gateway Package Version is: " +
          pkg_resources.get_distribution("thingsboard-gateway").version)
    TBModuleLoader.PATHS.append(path_extension)
    global gateway
    gateway = TBGatewayService(path_cofig)

    signal.pause()


@app.command()
def init():
    output_dir = Path.cwd()
    with resources.as_file(resources.files(templates)) as template_path:
        for item in template_path.rglob('*'):
            if item.is_file():
                relative_path = item.relative_to(template_path)
                destination = output_dir / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(item, destination)
                typer.echo(f"✅ Copied: {relative_path}")

    typer.echo("🎉 All template files copied successfully.")
    


