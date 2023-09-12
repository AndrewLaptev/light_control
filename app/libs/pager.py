import os


class Pager:
    def __init__(self, dir_path: str) -> None:
        self.dir_path = dir_path
        self.pages: dict[str, str] = dict()

        for filepath in os.listdir(dir_path):
            with open(os.path.join(dir_path, filepath), "r") as file:
                filename = os.path.basename(file.name)
                self.pages[filename.replace(".html", "")] = file.read()

    def get_page(self, name: str) -> str:
        return self.pages[name]
