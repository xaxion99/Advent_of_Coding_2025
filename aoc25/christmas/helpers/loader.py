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