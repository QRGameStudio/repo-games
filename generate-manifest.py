from collections import OrderedDict
from pathlib import Path
import json

DIR_ROOT = Path(__file__).resolve().parent.absolute()


def load_game_manifest(dir_game: Path) -> dict:
    try:
        file_manifest = next(dir_game.glob("*.manifest.json"))
        compiled_content = next(dir_game.glob("*.compiled.txt")).read_text().strip()
    except StopIteration:
        return {}

    try:
        file_qr = next(dir_game.glob("*.svg"))
    except StopIteration:
        file_qr = None

    data = json.loads(file_manifest.read_text())
    if file_qr:
        data["url"] = f"https://qgo.eu/GAME/#{compiled_content}"
        data["qr"] = True
    else:
        game_id = data["id"]
        data["url"] = f"https://qrpr.eu/html#RD{game_id}"
        data["qr"] = False
    return {data["id"]: data}


def load_manifest() -> dict:
    manifest = {}
    for dir_game in sorted(DIR_ROOT.glob("*/"), key=lambda x: x.name):
        manifest.update(load_game_manifest(dir_game))
    return manifest


def generate_md_table(manifest: dict) -> str:
    table = "| Name | Version | Play |\n"
    table += "|------|---------|------|\n"
    for data in manifest.values():
        table += f"| {data['name']} | {data['version']} | [Play]({data['url']}) |\n"
    return table


def write_md(manifest: dict):
    table = generate_md_table(manifest)
    with open(DIR_ROOT / "README.md", "w") as f:
        f.write("# Published QR Games\n\n")
        f.write(table)


def write_json(manifest: dict):
    with open(DIR_ROOT / "manifest.json", "w") as f:
        json.dump(OrderedDict(manifest), f, indent=1)


def main():
    manifest = load_manifest()
    write_md(manifest)
    write_json(manifest)


if __name__ == "__main__":
    main()
