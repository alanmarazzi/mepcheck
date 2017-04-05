import argparse
from mepcheck import EUvotes, get_meps

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", type=str, help="Add a country to see MEPs from that member State")
    parser.add_argument('--mep', type=int, help="Pass a MEP id and see the last 50 votes")
    parser.add_argument("--limit", type=int, help="Decide how many votes to return by passing an int")
    parser.add_argument("-s", "--summary", action="store_true", help="Return only the summary of votes")
    args = parser.parse_args()
    if args.country is None and args.mep is None:
        get_meps()
    elif args.country is not None and args.mep is None:
        get_meps(args.country)
    elif args.country is None and args.mep is not None:
        if args.limit is None:
            votes = EUvotes(mep_id=args.mep, limit=50)
            votes.print_attendance(summary=args.summary)
        else:
            votes = EUvotes(mep_id=args.mep, limit=args.limit)
            votes.print_attendance(summary=args.summary)
    else:
        print("Use --help to see how to use MEPcheck CLI")
