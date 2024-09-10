# postura-project

## Setting up the virtual environment
- On macOS and Linux:
```bash
python -m venv myenv
source myenv/bin/activate
```

- On Windows:
```shell
python -m venv myenv
myenv\Scripts\activate
```

## Managing dependencies
1. Install existing dependencies from `requirement.txt` file:
```bash
pip install -r requirements.txt
```

2. Install any new dependency if needed:
```bash
pip install <lib>
```

3. Re-generate the requirements file:
```bash
pip freeze > requirements.txt
```