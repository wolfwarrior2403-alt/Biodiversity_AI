# BioSight AI

BioSight AI is a Streamlit prototype that uses BioCLIP to predict the taxonomic identity of biodiversity images.

## Quick start

1. Create and activate a Python environment (recommended):

```bash
python -m venv .venv
# On Windows PowerShell
.venv\Scripts\Activate.ps1
# On Windows (cmd)
.venv\Scripts\activate.bat
# On Unix / macOS
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the app:

```bash
python -m streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Usage

- Upload a biodiversity image (JPG/PNG) using the uploader.
- The app will run BioCLIP and display the top prediction, match score, and taxonomic details.

## Recent UI note

The prediction card was simplified to remove the "Most likely biological match" label. It now displays a cleaner card, for example:

```
🌿 Tiger

Panthera tigris

────────────────────

Family: Felidae
```

## Dependencies

At minimum, the app requires:

- streamlit
- pandas
- pillow
- bioclip (or the package you use for the TreeOfLifeClassifier)

If you don't have a `requirements.txt`, create one with these lines:

```
streamlit
pandas
pillow
bioclip
```

## Continuous integration

This repository includes a basic GitHub Actions workflow that checks Python syntax and runs `flake8` on pushes and pull requests to `main`.

Build status: ![CI](https://github.com/wolfwarrior2403-alt/Biodiversity_AI/actions/workflows/ci.yml/badge.svg)

## Contributing

Suggestions, bug reports and improvements are welcome. Open an issue or submit a pull request.

## License

This project is provided as a prototype without an explicit license.
