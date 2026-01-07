import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

class HDFSStorage:
    """HDFS or simulated distributed storage"""

    def __init__(self, base_path, use_real_hdfs=False):
        self.base_path = base_path
        self.use_real_hdfs = use_real_hdfs

        if not use_real_hdfs:
            # Create local directories simulating HDFS
            import os
            os.makedirs(f"{base_path}/stock_data", exist_ok=True)
            os.makedirs(f"{base_path}/sentiment_data", exist_ok=True)
            os.makedirs(f"{base_path}/processed_data", exist_ok=True)
            print("HDFS simulation directories created")
        else:
            print("Using real HDFS")

    def write_parquet(self, data, path):
        """Write data to HDFS as Parquet"""
        try:
            full_path = f"{self.base_path}/{path}"

            if isinstance(data, pd.DataFrame):
                table = pa.Table.from_pandas(data)
                pq.write_table(table, full_path)
                print(f"Written to HDFS: {full_path}")
            else:
                print(f"Data must be DataFrame")

        except Exception as e:
            print(f"HDFS write error: {e}")

    def read_parquet(self, path):
        """Read data from HDFS"""
        try:
            full_path = f"{self.base_path}/{path}"
            table = pq.read_table(full_path)
            df = table.to_pandas()
            print(f"Read from HDFS: {full_path}")
            return df
        except Exception as e:
            print(f"HDFS read error: {e}")
            return None
