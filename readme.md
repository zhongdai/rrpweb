# Research Request Portal

## Quick Start

### Export Flask environment variables

```bash
export FLASK_APP=you/path/to/app.py
export FLASK_DEBUG=1
```

### Run follow commands

```bash
flask db init
flask db migrate
```

### Insert dummy records

```bash
python makd_dummy_data.py
```

### Launch the app

```bash
flask run
```

> under the first `rrp` folder

## TODO

1. [x] Add the dummy data
2. [ ] Add test cases
3. [x] Add logic to save requests
4. [ ] Improve the CSS
5. [ ] Protect the password