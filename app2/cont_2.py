from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import os

app = FastAPI()

class CSVItem(BaseModel):
    file: str
    product: str

@app.post("/process_csv")
async def process_csv(item: CSVItem):
    if not os.path.isfile("/mohammed_PV_dir/"+item.file):
        #raise HTTPException(status_code=404, detail={"file": item.file, "error": "File not found."})
        return {"file": item.file, "error": "File not found."}

    try:
        with open("/mohammed_PV_dir/"+item.file, mode='r') as csv_file:
            first_char = csv_file.read(1)
            if not first_char:
                raise ValueError("File is empty")

            csv_file.seek(0)

            # Read the file into a list of dictionaries, stripping any whitespace
            csv_reader = csv.DictReader((line.strip() for line in csv_file))

            # Strip whitespace from the fieldnames
            csv_reader.fieldnames = [name.strip() for name in csv_reader.fieldnames]

            if (csv_reader.fieldnames != ['product', 'amount']):
                raise ValueError("CSV headers not as expected. Expected ['product', 'amount']")

            total_amount = 0
            for row in csv_reader:
                if 'product' in row and 'amount' in row:
                    if row['product'] == item.product:
                        total_amount += int(row['amount'].strip())
                else:
                    raise ValueError("CSV rows not as expected. Each row should have 'product' and 'amount'")

    except Exception as e:
        #raise HTTPException(status_code=400, detail={"file": item.file, "error": "Input file not in CSV format."})
        return {"file": item.file, "error": "Input file not in CSV format."}

    return {"file": item.file, "sum": total_amount}

if __name__ == "__main__":
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    import asyncio

    config = Config()
    config.bind = ["0.0.0.0:6001"]
    asyncio.run(serve(app, config))

# demo commit
