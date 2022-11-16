from pathlib import Path
from rich.progress import track


def get_files(input: Path, kind: str = "pdf", fullname: str = "", key=None):
    if fullname:
        if key:
            return {
                key(x): str(x).replace(str(input), "")
                for x in input.glob(f"**/{fullname}")
                if not x.name.startswith(".")
            }
        return {
            x.stem: str(x).replace(str(input), "")
            for x in input.glob(f"**/{fullname}")
            if not x.name.startswith(".")
        }

    return {
        x.stem: str(x).replace(str(input), "")
        for x in input.glob(f"**/*.{kind}")
        if not x.name.startswith(".")
    }


def _sort_pdf(*args, **kwargs):
    if isinstance(kwargs["file"], str):
        kwargs["file"] = Path(kwargs["file"])
    name = kwargs["file"].stem.upper() + kwargs["file"].suffix.lower()
    return kwargs["output"] / f"{kwargs['kind']}/{name}"


def _sort_txt(*args, **kwargs):
    if isinstance(kwargs["file"], str):
        kwargs["file"] = Path(kwargs["file"])
    name = kwargs["file"].name.lower()
    parts = name.split("_")
    parent = parts[1].upper()
    name = parts[0] + "_" + parent + kwargs["file"].suffix.lower()
    # Path(name).mkdir(parents=True, exist_ok=True)
    return kwargs["output"] / f"{kwargs['kind']}/{parent}/{name}"

def _sort_tif(*args, **kwargs):
    if isinstance(kwargs["file"], str):
        kwargs["file"] = Path(kwargs["file"])
    name = kwargs["file"].name
    parts = name.split("_")
    parent = parts[1].upper()
    name = parts[0] + "_" + parent + kwargs["file"].suffix.lower()
    # Path(parent).mkdir(parents=True, exist_ok=True)
    return kwargs["output"] / f"{kwargs['kind']}/{parent}/{name}"


def consolidate_files(lst, input, output, kind="pdf", sorter_func=None) -> None:
    # make all parent folders
    [
        (output / f"{kind}/{Path(x).name}").parent.mkdir(parents=True, exist_ok=True)
        for x in lst
    ]

    # copy all files
    if sorter_func:
        [
            (input / x.lstrip("/")).copy(
                sorter_func(file=x, input=input, output=output, kind=kind)
            )
            for x in track(
                lst, description=f"Consolidating {len(lst)} {kind} files in {input}..."
            )
            if not (output / f"{kind}/{Path(x).name}").exists()
        ]
        return
    [
        (input / x.lstrip("/")).copy((output / f"{kind}/{Path(x).name}"))
        for x in track(
            lst, description=f"Consolidating {len(lst)} {kind} files in {input}..."
        )
        if not (output / f"{kind}/{Path(x).name}").exists()
    ]
    return


def consolidate_guides(guide_files, input, output, kind="pdf"):
    for number, source in guide_files.items():
        source = input / source.lstrip("/")
        target = output / f"guides-{kind}/{number}.{kind}"
        Path(source).copy(target) if not target.exists() else None
