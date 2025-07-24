from pathlib import Path
import pandas as pd
import pdfminer.high_level


def process_file(path: Path, content_type: str) -> str:
    try:
        if content_type == "text/csv":
            df = pd.read_csv(path)
            return df.to_json(orient="records")
        if content_type in [
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ]:
            df = pd.read_excel(path)
            return df.to_json(orient="records")
        if content_type == "application/pdf":
            text = pdfminer.high_level.extract_text(path)
            return text
    except Exception as e:
        return f"error:{e}"
    return ""
