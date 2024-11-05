import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Parse command-line arguments.")
parser.add_argument("-e", type=int, help="Parameter e")
parser.add_argument("-d", type=int, help="Parameter d")
parser.add_argument("-th", type=int, help="Parameter threshold")

# Parse arguments
args = parser.parse_args()

# Print the values of e, d, and th
print(args.e, args.d, args.th)