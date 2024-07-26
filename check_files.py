from string import ascii_lowercase
from subprocess import check_output
from pathlib import Path
from jinja2 import Template


def save_file(file, data):
    with open(file, "wt") as f:
        f.write(data)

def read_file(file):
    with open(file, "rt") as f:
        return f.read()


def main():
    ok, not_ok = 0,0
    for chall_dir in filter(lambda p: p.is_dir(), Path('.').iterdir()):
        chall_dir: Path
        if chall_dir.name.startswith('.'): continue
        c = str(chall_dir.name)

        container_name = f'test-{c}-1'
        output = check_output(f"docker exec {container_name} sh -c 'cat /srv/app/flag.txt || cat /srv/flag.txt || true'", text=True, shell=True)

        flag = chall_dir / 'private' / 'flag.txt'
        expected = flag.read_text()
        if expected != output:
            print(f'task: {c}, expected: {expected}, output: {output}')
            not_ok += 1
        else:
            ok += 1

    print(f'ok: {ok}, not_ok: {not_ok}')


def change_flags():
    for chall_dir in filter(lambda p: p.is_dir(), Path('.').iterdir()):
        chall_dir: Path
        if chall_dir.name.startswith('.'): continue

        flag = chall_dir / 'private' / 'flag.txt'
        flag.write_text(str(chall_dir.name)*32)



def rename_dirs():
    for chall_dir, new_name in zip(filter(lambda p: p.is_dir(), Path('.').iterdir()), ascii_lowercase):
        chall_dir: Path
        if chall_dir.name.startswith('.'): continue

        chall_dir.rename(new_name)


def generate_compose_file():
    ch = {}
    for idx, chall_dir in enumerate(filter(lambda p: p.is_dir(), Path('.').iterdir())):
        chall_dir: Path
        if chall_dir.name.startswith('.'): continue

        n = str(chall_dir.name)
        ch[n] = {
            'enabled': True,
            'port': 10000+idx,
        }

    rendered = Template(read_file('./docker-compose.yml.jinja')).render(
        tasks=ch.items()
    )
    save_file('./docker-compose.yml', rendered)

if __name__ == '__main__':
    main()
    # rename_dirs()
    # change_flags()
    # generate_compose_file()

