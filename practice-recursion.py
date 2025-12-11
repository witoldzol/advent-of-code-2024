import json

data = """[{"name": "Joe",
  "age": "21",
  "children": [{
    "name": "Smith",
    "age": "42",
    "children": []
  }, {
    "name": "Gary",
    "age": "21",
    "children": [{
      "name": "Jenifer",
      "age": "23",
      "children": [{
        "name": "Dani",
        "age": "32",
        "children": []
      }, {
        "name": "Max",
        "age": "34",
        "children": []
      }]
    }]
  }]
}, {
  "name": "Albert",
  "age": "33",
  "children": []
}, {
  "name": "Ron",
  "age": "29",
  "children": []
}]
"""
data = json.loads(data)


def traverse(node, accumulator):
    if isinstance(node, list):
        for item in node:
            traverse(item, accumulator)
    elif isinstance(node, dict):
        keys_to_keep = {"name", "age"}
        copy_of_dict = {k: v for k, v in node.items() if k in keys_to_keep}
        accumulator.append(copy_of_dict)
        for k, v in node.items():
            traverse(v, accumulator)
    else:
        print("its a primitive, moving on")
        print(node)


accumulator = []

traverse(data, accumulator)
print("<" * 100)
print(f"{accumulator=}")
print(">" * 100)
