def read_test_file(name):
    d = {
        4: "txt",
        12: "png"
    }
    with open(f"./static/texts_for_tests/{name}.{d[name]}", encoding='utf-8') as file:
        data = [i.strip() for i in file.readlines()]
        return data


def read_theory_file(name):
    with open(f"./static/theories/{name}.txt", encoding='utf-8') as file:
        data = file.read()
        return data

