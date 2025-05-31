

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


@app.command("check-utf")
def check_utf(
    ip: Annotated[str, typer.Option(help="IP address of the device.")],
    password: Annotated[str, typer.Option(help="Devise access key.")],
):
    """Check if possible to write UTF8 text
    """
    devices.zk_devices_check_utf8(ip, password)


@app.command("get-attendance")
def _get_attendance(
    ip: Annotated[str, typer.Option(help="IP address of the device.")],
    password: Annotated[str, typer.Option(help="Devise access key.")],
):
    """Get attendances"""
    devices.zk_devices_get_attendance(ip, password)


@app.command("user-info")
def _show_user_info_cmd(
    ip: Annotated[str, typer.Option(help="IP address of the device.")],
    password: Annotated[str, typer.Option(help="Devise access key.")],
):
    """Shows user infor"""
    devices.zk_devices_get_user_info(ip, password)


if __name__ == "__main__":
    app()
