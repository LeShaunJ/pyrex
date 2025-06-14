Contributing
============

Contributions are welcome; just open [an issue](https://github.com/LeShaunJ/clo/issues/new) or send us a pull request.

## Virtual Environment

Ensure you're using `venv` or similar to isolate your environment:

```bash
python3 -m venv .venv
activate
```

If you use [`ops`](https://github.com/nickthecook/crops):

```bash
ops up
ops python [...] # run python commands or REPL
```

## Testing

Executing the test in your environment:

```bash
pip install -e .
flake8
pytest
```

or with [tox](https://pypi.org/project/tox) installed:

```bash
tox
```
