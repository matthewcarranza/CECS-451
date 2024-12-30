import sys


def main(args):
    if len(args) != 1:
        print("Usage: python hmm.py <file>")
        sys.exit(0)
    file = args[0]
    params = []
    with open(file, 'r') as infile:
        for line in infile:
            params.append(line.strip().split(","))

    for line in params:
        e = []
        a, b, c, d, f = 0, 0, 0, 0, 0
        for j, n in enumerate(line):
            if j == 0: a = float(n)
            if j == 1: b = float(n)
            if j == 2: c = float(n)
            if j == 3: d = float(n)
            if j == 4: f = float(n)
            if j >= 5: e.append(n)
            
        prev1 = a
        prev0 = 1 - a
        p1 = 0
        p0 = 0

        for i, et in enumerate(e):
            if i >= 1:
                prev1 = p1
                prev0 = p0
            if et == 't':
                p1 = d * (b * prev1 + c * prev0)
                p0 = f * ((1 - b) * prev1 + (1 - c) * prev0)
            else:
                p1 = (1-d) * (b * prev1 + c * prev0)
                p0 = (1-f) * ((1 - b) * prev1 + (1 - c) * prev0)

            norm = p1 + p0

            p1 = p1/norm
            p0 = p0/norm

        for n in line[:len(line)-1]:
            print(f"{n},", end='')
        print(f"{line[len(line)-1]}--><{p1:.4f},{p0:.4f}>")


if __name__ == "__main__":
    main(sys.argv[1:])
