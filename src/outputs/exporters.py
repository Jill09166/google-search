thonimport json
from pathlib import Path
import logging
from datetime import datetime

class JSONExporter:
    def export(self, data):
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = output_dir / f"results_{timestamp}.json"

        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Error exporting JSON: {e}")
            return None

        return file_path