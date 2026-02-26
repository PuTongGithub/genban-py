import json
from pathlib import Path
from typing import List


# 文件存储底层操作类
class _FileStorage:

    # 追加写入 JSONL 文件
    def appendToJsonl(self, filePath: Path, records: List[dict]) -> None:
        if not records:
            return

        filePath.parent.mkdir(parents=True, exist_ok=True)

        with open(filePath, "a", encoding="utf-8") as f:
            for record in records:
                jsonLine = json.dumps(record, ensure_ascii=False)
                f.write(jsonLine + "\n")

    # 读取 JSONL 文件，解析错误抛异常
    def readJsonl(self, filePath: Path) -> List[dict]:
        if not filePath.exists():
            return []

        records = []
        with open(filePath, "r", encoding="utf-8") as f:
            for lineNum, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError as e:
                    raise json.JSONDecodeError(
                        f"JSONL parse error at {filePath}:{lineNum}",
                        e.doc,
                        e.pos
                    )

        return records

    # 列出指定日期范围内的 JSONL 文件
    def listJsonlFiles(self, dirPath: Path, startDate: str, endDate: str) -> List[Path]:
        if not dirPath.exists():
            return []

        files = []
        for filePath in dirPath.glob("*.jsonl"):
            dateStr = filePath.stem
            if startDate <= dateStr <= endDate:
                files.append(filePath)

        files.sort(key=lambda p: p.stem)
        return files


fileStorage = _FileStorage()
