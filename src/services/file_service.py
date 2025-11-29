from typing import Iterator


def get_file_iterator(file_path: str, start: int, end: int, chunk_size: int = 1024 * 1024) -> Iterator[bytes]:
    with open(file_path, 'rb') as file:
        file.read(start)
        remaining_bytes = end - start + 1

        while remaining_bytes > 0:
            read_size = min(remaining_bytes, chunk_size)
            data = file.read(read_size)
            if not data:
                break
            yield data
            remaining_bytes -= len(data)
