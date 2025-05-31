#!/usr/bin/python3
import os


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


# signal.signal(signal.SIGINT, signal_handler)


@app.command()
def main(path_cofig: str):
    f = Figlet(font='big')
    print(f.renderText('Odoonix'))
    print("Thingsboard Gateway Package Version is: " +
          pkg_resources.get_distribution("thingsboard-gateway").version)

    current_file_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_file_path)
    TBModuleLoader.PATHS.append(
        os.path.join(current_folder, "extensions")
    )
    global gateway
    gateway = TBGatewayService(path_cofig)

    signal.pause()


TEMPLATE_FILES = [
    "conf.json",
    "logs.json",
    "statistics.json",
    "devices/cups.json",
    "devices/zktec.json",
]


@app.command()
def init():
    output_dir = Path.cwd()
    files_root = resources.files(templates)

    for relative_path_str in TEMPLATE_FILES:
        relative_path = Path(relative_path_str)
        file_in_package = files_root / relative_path

        if not file_in_package.is_file():
            typer.echo(f"Skipping: {relative_path} (not a file)")
            continue

        with resources.as_file(file_in_package) as real_file:
            destination = output_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(real_file, destination)
            typer.echo(f"Copied: {relative_path}")

    typer.echo("Selected template files copied successfully.")


if __name__ == "__main__":
    app()
