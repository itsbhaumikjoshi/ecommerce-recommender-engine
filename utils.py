import json
import os
import pandas as pd
from datetime import datetime

def create_chunks(chunk_size, total_chunks):
  for i, chunk in enumerate(pd.read_json("./train.jsonl", lines=True, chunksize=chunk_size)):
    if does_file_exists(f'./chunks/chunk_{i+1}.json'):
      print(f"chunk_{i+1} already exists.")
    else:
      print(f"creating the {i+1} chunk.")
      # fixes the data to a desired form.
      df = normalize_data(chunk, i+1)
    if i+1 == total_chunks:
      break

def does_file_exists(name: str) -> bool:
  return os.path.exists(name)

# normalize the (session, events) columns to (session, type, aid, ts) columns
def normalize_data(df: pd.DataFrame, chunk_number: int) -> pd.DataFrame:
    data = []
    for _, row in df.iterrows():
         if row.get("events") is not None:
            for event in row.get("events"):
                data.append({
                    "session": row.get("session"),
                    "aid": event.get("aid"),
                    "type": event.get("type"),
                    "timestamp": str(datetime.utcfromtimestamp(event.get("ts") / 1000)),
                })
         else:
             data.append({ "session": row.get("session") })

    # saving the df as df.to_json and opening the file occupies more RAM space than the actual file size.         
    with open(f"./chunks/chunk_{chunk_number}.json", "w") as outfile:
        outfile.write(json.dumps(data))
      
    return pd.DataFrame(data)
