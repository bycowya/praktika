import pandas as pd
import json


def export_csv(results, columns):
    df = pd.DataFrame(results, columns=columns)
    return df.to_csv(index=False).encode("utf-8")


def export_json(results, columns):
    data = [dict(zip(columns, row)) for row in results]
    return json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")