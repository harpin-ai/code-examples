__1. Create and activate a virtual environment:__

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Or on Windows
# venv\Scripts\activate
```

__2. Install dependencies:__

```bash
# Install packages from requirements.txt
pip install -r requirements.txt
```

__3. Set environment variables:__

```bash
# Set required authentication variables
export CLIENT_ID="your_client_id_here"
export REFRESH_TOKEN="your_refresh_token_here"

# Optional: Set source configuration (for create_source.py)
export SOURCE_NAME="My Identity Source"
export SOURCE_DESCRIPTION="Custom identity data source"
```

__4. Run the scripts:__

__To create and enable a source:__

```bash
python create_source.py
```

__To ingest data (after creating a source):__

```bash
# Set the source ID returned from create_source.py
export SOURCE_ID="source_id_from_previous_step"
python ingest.py
```

The `create_source.py` script will display the source ID at the end, which you can then use to set the `SOURCE_ID` environment variable for the ingestion script.
