from .pathlib import Path


def log(lsts):
    txt = ""
    for name, lst in lsts.items():
        txt += f"# Files moved\n"
        txt += f"## {name}\n"
        txt += "\n- " + "\n- ".join(lst)
        txt += "\n"

    Path("log.md").write_text(txt)
