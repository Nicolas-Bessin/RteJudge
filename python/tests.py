from pelicoparser import parser

print(parser("../sujet/real_tiny.json", "../sujet/real_tiny_solution.json"))
print(parser("../sujet/medium.json", "../sujet/medium_solution.json"))
print(parser("../sujet/large.json", "../sujet/large_solution.json"))
print(parser("../sujet/huge.json", "../sujet/huge_solution.json"))


# print(parser("../sujet/tiny.json", "../sujet/tiny-sol2.json"))

nb_tests = 36

with open("../Tests_fail/Descriptions.txt") as desc:
    for i in range(1, nb_tests + 1):
        print(desc.readline(), end="")
        print(parser("../sujet/tiny.json", f"../Tests_fail/test{i}.json"))
