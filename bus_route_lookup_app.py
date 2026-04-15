import pandas as pd
import os
import sys

# ── Configuration ────────────────────────────────────────────────────────────
# Update this path if you move the data file
DATA_FILE = "bmtc_routes_with_stops.csv"
SEPARATOR = " -> "


# ── Data loading ─────────────────────────────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    """Load the BMTC routes Excel/CSV file into a DataFrame."""
    if not os.path.exists(filepath):
        print(f"[ERROR] Data file not found: {filepath}")
        sys.exit(1)
    try:
        df = pd.read_excel(filepath)
    except Exception:
        df = pd.read_csv(filepath)
    df.columns = [c.strip() for c in df.columns]
    return df


# ── Core lookup ───────────────────────────────────────────────────────────────
def find_routes(df: pd.DataFrame, bus_number: str) -> list[dict]:
    """
    Return all routes whose Route column matches bus_number (case-insensitive).
    Each result dict has: route, stops (list), start, destination.
    """
    query = bus_number.strip().upper()
    mask = df["Route"].astype(str).str.strip().str.upper() == query
    matches = df[mask]

    results = []
    for _, row in matches.iterrows():
        raw_stops = str(row["Stops (via)"]).strip()
        stops = [s.strip() for s in raw_stops.split(SEPARATOR) if s.strip()]
        results.append(
            {
                "route": row["Route"],
                "stops": stops,
                "start": stops[0] if stops else "N/A",
                "destination": stops[-1] if stops else "N/A",
            }
        )
    return results


# ── Display ───────────────────────────────────────────────────────────────────
def display_route(result: dict, index: int = 0, total: int = 1) -> None:
    """Pretty-print a single route result."""
    header = f"  Route: {result['route']}"
    if total > 1:
        header += f"  ({index + 1} of {total} variants)"

    width = 65
    print("\n" + "═" * width)
    print(header)
    print("═" * width)
    print(f"  🟢  Start       : {result['start']}")
    print(f"  🔴  Destination : {result['destination']}")
    print(f"  🚌  Total Stops : {len(result['stops'])}")
    print("─" * width)
    print("  STOP-BY-STOP ROUTE FLOW:")
    print("─" * width)

    for i, stop in enumerate(result["stops"]):
        if i == 0:
            prefix = "  🟢 START  "
        elif i == len(result["stops"]) - 1:
            prefix = "  🔴 END    "
        else:
            prefix = f"  {i:>3}.       "
        print(f"{prefix} {stop}")
        if i < len(result["stops"]) - 1:
            print("              ↓")

    print("═" * width)


def list_all_routes(df: pd.DataFrame) -> None:
    """Print the first 20 unique route names as a hint."""
    routes = df["Route"].astype(str).str.strip().unique()
    print(f"\n  Total routes in dataset: {len(routes)}")
    print("  Sample routes:", ", ".join(routes[:20]), "…")


# ── Main interaction loop ─────────────────────────────────────────────────────
def main() -> None:
    print("\n" + "=" * 65)
    print("        BMTC BUS ROUTE LOOKUP")
    print("=" * 65)

    df = load_data(DATA_FILE)
    print(f"  ✅ Loaded {len(df)} routes from '{DATA_FILE}'")

    while True:
        print()
        bus_input = input("  Enter bus number (or 'list' to browse / 'quit' to exit): ").strip()

        if bus_input.lower() in ("quit", "exit", "q"):
            print("\n  Goodbye! 🚌\n")
            break

        if bus_input.lower() == "list":
            list_all_routes(df)
            continue

        if not bus_input:
            print("  ⚠  Please enter a bus number.")
            continue

        results = find_routes(df, bus_input)

        if not results:
            print(f"\n  ❌ No route found for bus number '{bus_input}'.")
            print("     Tip: type 'list' to see available routes.")
            continue

        for idx, result in enumerate(results):
            display_route(result, index=idx, total=len(results))


if __name__ == "__main__":
    main()
