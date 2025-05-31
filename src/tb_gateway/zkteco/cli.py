

import typer
from typing_extensions import Annotated

from tb_gateway.zkteco import devices

app = typer.Typer()


@app.command()
def check(
    ip: Annotated[str, typer.Option(help="IP address of the device.")],
    password: Annotated[str, typer.Option(help="Devise access key.")],
):
    """Checks connection to the ZK devices
    """
    devices.zk_devices_check_connection(ip, password)


@app.command()
def list():
    """List installed devices
    """
    print("Not implemented")

if __name__ == "__main__":
    app()
