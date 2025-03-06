from datetime import datetime
from io import BytesIO
from queue import Queue
from os import getenv
from typing import cast
from node import CompanyNode, QueueNode
import requests
import fitz

def download_pdfs_worker(url_root: str, urls: list[str], company: CompanyNode, pdf_queue: Queue) -> None:
    pdfs = []

    for url in urls:
        response = requests.get(f"{url_root}{url}")
        pdfs.append(QueueNode(company=company, data=response.content))

    for pdf in pdfs:
        if pdf.data is not None:
            pdf_queue.put(pdf)

def scrape_and_process_pdfs(finished_scanning: bool, pdf_queue: Queue) -> None:
    output_directory = getenv("OUTPUT_DIRECTORY")

    if output_directory is None or len(output_directory) == 0:
        raise Exception("OUTPUT_DIRECTORY environment variable is not set")

    rows = []
    now = datetime.now()
    year_columns = [f"{now.year - index}" for index in range(0, 11)]

    while (not finished_scanning) or (not pdf_queue.empty()):
        if pdf_queue.empty():
            continue

        item: QueueNode = pdf_queue.get()
        new_row = f"{item.company.name},{item.company.industry},"
        data_buffer = BytesIO(cast(bytes, item.data))
        pdf_doc = fitz.open(stream=data_buffer)
        pdf_page = pdf_doc.load_page(0)
        pdf_blocks = pdf_page.get_text("dict").get("blocks")

        for block in pdf_blocks:

        rows.append(new_row)

    with open(f"{output_directory}/{now.strftime("%Y%m%d%H%M%S")}_value_line_current_issue_pdf_scrape_.csv", "w") as output_file:
        output_file.write(f"name,industry,{','.join(year_columns)},average_estimate_next_year;\n")
        output_file.writelines(rows)
        output_file.close()
