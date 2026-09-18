import sys

# Import modules from their respective folders
from scraper import extract
from processing import transform
from database import load

def run_pipeline():
    print("=" * 50)
    print("Starting End-to-End Data Pipeline")
    print("=" * 50)

    # 1. Extraction Phase
    print("\n[Step 1/3]: Extraction Phase")
    try:
        extract.main()
    except Exception as e:
        print(f"Extraction failed: {e}")
        sys.exit(1)

    # 2. Transformation Phase
    print("\n" + "=" * 50)
    print("[Step 2/3]: Transformation Phase")
    try:
        transform.main()
    except Exception as e:
        print(f"Transformation failed: {e}")
        sys.exit(1)

    # 3. Loading Phase
    print("\n" + "=" * 50)
    print("[Step 3/3]: Loading Phase")
    try:
        load.main()
    except Exception as e:
        print(f"Loading failed: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Data Pipeline Completed Successfully!")
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()