from tqdm import tqdm
from config import BATCH_SIZE
import contextlib
import math

class DummyFile:
    def write(self, x):
        if x.strip():
            tqdm.write(x)
    def flush(self):
        pass

def batch_insert(vector_store, documents, ids, batch_size=BATCH_SIZE):
    total_batches = math.ceil(len(documents) / batch_size)
    for batch_no, i in (pbar := tqdm(enumerate (range(0, len(documents), batch_size), start=1), total=total_batches, desc="Inserting documents")):
        pbar.set_postfix(docs=f" {i} - {min(i + batch_size, len(documents))}")
        batch_doc = documents[i : i + batch_size]
        batch_ids = ids[i : i + batch_size]
        try:
            with contextlib.redirect_stdout(DummyFile()), contextlib.redirect_stderr(DummyFile()):
                vector_store.add_documents(documents=batch_doc, ids=batch_ids)
        except Exception as e:
            tqdm.write(f"Error inserting {batch_no} : {e}")
            continue
    tqdm.write(f"\n✅ All the reviews have been added successfully to the vector store now\n")

