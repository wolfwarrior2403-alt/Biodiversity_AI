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

## Docker image

You can build and run the application in Docker locally:

```bash
# Build
docker build -t your-dockerhub-username/biodiversity_ai:latest .

# Run
docker run -p 8501:8501 your-dockerhub-username/biodiversity_ai:latest
```

The repository also includes a GitHub Actions workflow that can publish a Docker image to Docker Hub. To enable it, add the following repository secrets:

- `DOCKERHUB_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — a Docker Hub access token or password

The workflow will push images to `<DOCKERHUB_USERNAME>/biodiversity_ai:latest` and a SHA-tagged image.

## Contributing

Suggestions, bug reports and improvements are welcome. Open an issue or submit a pull request.

## License

This project is provided as a prototype without an explicit license.
