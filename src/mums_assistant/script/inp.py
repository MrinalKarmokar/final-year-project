import sys

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "1":
        print("Circle")
    elif sys.argv[i] == "2":
        print("Square")
    else:
        print("Default")