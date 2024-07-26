

1. run containers with `docker compose -p test --profile enabled up --build --force-recreate`
2. to check whether `flag.txt` is correct in all containers run `python replace_flag.py`
3. if you get "ok: 14, not_ok: 0", repeat steps 1 and 2
