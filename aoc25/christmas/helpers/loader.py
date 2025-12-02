class Loader:
    @staticmethod
    def load_lines(path: str):
        lines = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
        return lines

    @staticmethod
    def load_csv_row(path: str):
        with open(path, "r", encoding="utf-8") as f:
            row = f.read().strip()
        return [item.strip() for item in row.split(",") if item.strip()]
