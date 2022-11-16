from . import __app_name__
from .pathlib import Path
from .file_wrangling import (
    consolidate_files,
    consolidate_guides,
    _sort_pdf,
    _sort_txt,
    _sort_tif,
    get_files,
)
from .log import log
from .patterns import NUMBER

import click
import pandas as pd
import fitz
import re
from pathlib import Path


@click.command(name=__app_name__)
@click.option(
    "--input",
    type=click.Path(exists=True),
    prompt="Input UKDS data (directory)",
    help="The input path where the UKDS trade directories can be found.",
)
@click.option(
    "--output",
    type=click.Path(exists=False),
    prompt="Output UKDS data (directory)",
    help="The output path where the consolidated UKDS trade directories should be located.",
)
@click.option(
    "--metadata",
    type=click.Path(exists=False),
    prompt="Metadata (CSV file)",
    help="The path to the CSV file with corresponding metadata.",
)
def main(input, output, metadata):
    """Simple app that wrangles the UKDS Trade Directories data folder."""

    # Ensure input, output are the correct type
    input, output = Path(input), Path(output)

    # 1. Consolidate files

    # 1a. PDF guides

    pdf_guides = get_files(
        input,
        fullname="guide.pdf",
        key=lambda x: NUMBER.search(str(x.parent.parent.parent)).groups()[0],
    )
    consolidate_guides(pdf_guides, input, output, kind="pdf")

    # 1b. HTML guides

    html_guides = get_files(
        input,
        fullname="*Information.htm",
        key=lambda x: NUMBER.search(str(x)).groups()[0],
    )
    consolidate_guides(html_guides, input, output, kind="html")

    # 1c. PDF files
    pdf_files = get_files(input, kind="pdf")
    consolidate_files(
        pdf_files.values(), input, output, kind="pdf", sorter_func=_sort_pdf
    )

    # 1d. text files
    txt_files = get_files(input, kind="TXT")
    consolidate_files(
        txt_files.values(), input, output, kind="txt", sorter_func=_sort_txt
    )

    # 1d. tiff files
    txt_files = get_files(input, kind="tif")
    consolidate_files(
        txt_files.values(), input, output, kind="tif", sorter_func=_sort_tif
    )

    # Add the log
    log(
        {
            "txt_files": txt_files,
            "pdf_files": pdf_files,
            "html_guides": html_guides,
            "pdf_guides": pdf_guides,
        }
    )

    ######
    #
    # Below script to create a messy concatenated.csv document with all the information from the guide.pdf documents.
    #
    ######

    # convert PDF guides to txt

    path = "./files/UKDS_Versions-consolidated/guides-pdf"
    output = "./files/UKDS_Versions-converted/guides"
    OVERWRITE = True

    for pdf in Path(path).glob("*.pdf"):
        doc = fitz.open(pdf)  # open document
        text = ""
        for page in doc:  # iterate the document pages
            text += page.get_text()  # .encode("utf8")  # get plain text (is in UTF-8)

        # strip the beginning
        text = text[text.find("of the page images. ") + 20 :]

        output = Path(output)
        output.mkdir(parents=True, exist_ok=True)
        txt_doc = output / pdf.name.replace(".pdf", ".txt")
        if not txt_doc.exists() or OVERWRITE:
            txt_doc.write_text(text)

        # parse
        lines = [(x.startswith("SN "), x) for x in text.splitlines()]

        category = None
        _lines = []
        for line in lines:
            is_sn, text = line

            if is_sn:
                sn = text
                continue

            if text == "------ ":
                continue

            if text.strip() == "":
                continue

            if re.match(r"^Page \d+ of ", line[1]):
                continue

            _lines.append(text)

        lines = _lines

        item_id = 0
        items = {}
        new = False
        hold = ""
        for i, e in reversed(list(enumerate([("...." in x, x) for x in lines]))):
            has_cat, text = e
            if "----" in text:
                if item_id in items and not items[item_id]:
                    pass
                else:
                    item_id += 1
                items[item_id] = {}
                new = True
                continue
            if not has_cat:
                if new:
                    items[item_id]["Name"] = text
                    new = False
                    continue
                new = False
                hold = text + hold
                continue
            else:
                new = False
                category, _text = re.split(r"\.{4,200}", text)
                category = category.strip()
                items[item_id][category] = _text + hold
                hold = ""

        csv_doc = output / pdf.name.replace(".pdf", ".csv")
        df = pd.DataFrame(items).T
        df["id"] = pdf.stem
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df.to_csv(csv_doc)

    df = pd.concat(
        [pd.read_csv(f) for f in Path(output).glob("**/*.csv")], ignore_index=True
    )
    df.to_csv(output / "concatenated.csv")

    # TODO: continue working on processing metadata (in notebook...)
    df = pd.read_csv(metadata)
    identifiers = set(df.Identifier.to_list())
    print(identifiers)
    exit()


if __name__ == "__main__":
    main()
