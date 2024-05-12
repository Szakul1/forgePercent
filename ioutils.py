import ast

def load_data():
    data = []
    try:
        with open('data', 'r') as file:
            for line in file.readlines():
                data.append([item for _, item in ast.literal_eval(line)])
    except FileNotFoundError:
        pass
    return data

def save_data(data):
    with open('data', '+w') as file:
        file.write('\n'.join([str([item for item in enumerate(row)]) for row in data]))