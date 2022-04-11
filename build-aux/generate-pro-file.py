#!/usr/bin/env python
import argparse
import sys
from pathlib import Path
from typing import List


class ArgumentValidator:

    def __init__(self):
        self.errors = False

    def dont_have_errors(self):
        return not self.errors

    def validate_root_dir(self, directory: str):
        path = Path(directory).absolute()
        if not path.exists():
            self.errors = True
            error(f'Root directory \'{directory}\' does not exist')
        elif not path.is_dir():
            self.errors = True
            error(f'Root directory \'{directory}\' is not a directory')

    def validate_included_paths(self, paths: List[str]):
        for file in paths:
            path = Path(file).absolute()
            if not path.exists():
                self.errors = True
                error(f'Path to include \'{file}\' does not exist')


class ProFileGenerator:

    def __init__(self):
        self.all_files = []

    def glob_all(self, included_paths: List[str]):
        for path in included_paths:
            included_files = [p for p in Path(path).absolute().rglob('*') if p.is_file()]
            self.all_files.extend(included_files)

    def make_them_relative_to(self, root_dir: str):
        root = Path(root_dir).absolute()
        self.all_files = [p.relative_to(root) for p in self.all_files]

    def write_to(self, template_out: str):
        template = Path(template_out).resolve()
        content = []

        for file in sorted(self.all_files):
            extension = file.suffix
            if '.py' == extension:
                content.append(f'SOURCES += {file}')
            elif '.ts' == extension:
                content.append(f'TRANSLATIONS += {file}')
            else:
                print(f'Can not include file \'{file}\' into project file')

        content = '\n'.join(sorted(content))
        template.write_text(content, encoding='utf-8')


def error(message):
    print(message, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Create a .pro file for the project')
    parser.add_argument('--root-dir', type=str, required=True,
                        help='Root directory of the project')
    parser.add_argument('--out-file', type=str, required=True,
                        help='Name of the .pro file to generate')
    parser.add_argument('--include', type=str, action='append',
                        help='Name of the .pro file to generate')
    run(parser.parse_args())


def run(args):
    root_dir = args.root_dir
    template_target = args.out_file
    included = args.include

    we = ArgumentValidator()
    we.validate_root_dir(directory=root_dir)
    we.validate_included_paths(paths=included)

    if we.dont_have_errors():
        we = ProFileGenerator()
        we.glob_all(included_paths=included)
        we.make_them_relative_to(root_dir)
        we.write_to(template_target)


if __name__ == '__main__':
    main()
