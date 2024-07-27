from subprocess import check_output
from pathlib import Path


def main():
    ok, not_ok = 0, 0
    for chall_dir in filter(lambda p: p.is_dir(), Path('.').iterdir()):
        chall_dir: Path
        if chall_dir.name.startswith('.'): continue
        c = str(chall_dir.name)

        output = check_output(
            f"docker compose -p test exec {c} cat /flag.txt", text=True,
            shell=True)

        flag = chall_dir / 'private' / 'flag.txt'
        expected = flag.read_text()
        if expected != output:
            print(f'task: {c}, expected: {expected}, output: {output}')
            not_ok += 1
        else:
            ok += 1

    print(f'ok: {ok}, not_ok: {not_ok}')


def generate_compose_file():
    from jinja2 import Template

    ch = {}
    for idx, chall_dir in enumerate(filter(lambda p: p.is_dir(), Path('.').iterdir())):
        chall_dir: Path
        if chall_dir.name.startswith('.'): continue

        n = str(chall_dir.name)
        ch[n] = {
        }

    rendered = Template(Path('./docker-compose.yml.jinja').read_text()).render(
        tasks=ch.items()
    )
    Path('./docker-compose.yml').write_text(rendered)


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        generate_compose_file()
    else:
        main()
