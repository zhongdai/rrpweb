# Research Request Portal


## Quick Start


1. Export Flask environment variables


```bash
export FLASK_APP=you/path/to/app.py
export FLASK_DEBUG=1
```


2. Run follow commands


```bash
flask db init
flask db migrate
```

3. Insert dummy records

```bash
python makd_dummy_data.py
```

3. Launch the app

```bash
flask run
```
> under the first `rrp` folder

## TODO


1. Add the dummy data
2. Add test cases
3. Add logic to save requests