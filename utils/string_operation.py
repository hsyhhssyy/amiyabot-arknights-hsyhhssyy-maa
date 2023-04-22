import json
from typing import List, Dict, Any

def extract_json(string: str) -> List[Dict[str, Any]]:
    json_strings = []
    json_objects = []
    open_brackets = 0
    start_index = None

    for index, char in enumerate(string):
        if char == '{':
            open_brackets += 1
            if open_brackets == 1:
                start_index = index
        elif char == '}':
            open_brackets -= 1
            if open_brackets == 0:
                json_strings.append(string[start_index : index + 1])

    for json_str in json_strings:
        try:
            json_object = json.loads(json_str)
            json_objects.append(json_object)
        except json.JSONDecodeError as e:
            pass

    return json_objects


# input_string = "博士：兔兔你好。{\"reply\": \"你好博士。\", \"mental\": \"\", \"activity\": \"\"}"

# extracted_json = extract_json(input_string)

# print(extracted_json)