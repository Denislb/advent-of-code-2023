import re

def parse_input(filename):
    workflows = {}
    parts = []
    with open(filename) as f:
        for line in f:
            if not line.strip():
                break
            workflow_name, workflow = re.findall(r"(.*){(.*)}", line)[0]
            workflows[workflow_name] = []
            for step in workflow.split(','):
                parsed_step = re.findall(r"(.*)(>|<)(.*):(.*)", step)
                if not parsed_step:
                    workflows[workflow_name].append({"next": step, "operator": None})
                else:
                    workflows[workflow_name].append({"category": parsed_step[0][0], "operator": parsed_step[0][1],  "value": int(parsed_step[0][2]), "next": parsed_step[0][3]})
        workflows["R"] = [{"operator": "Rejected"}]
        workflows["A"] = [{"operator": "Accepted"}]
        for line in f:
            new_part = {}
            for value in re.findall(r"{(.*)}", line)[0].split(','):
                idx, v = value.split('=')
                new_part[idx] = int(v)
            parts.append(new_part)

    return workflows, parts

def part_one(workflows, parts):
    s = 0
    for part in parts:
        found = False
        current = workflows["in"]
        while True:
            for instruction in current:
                if not instruction["operator"]:
                    current = workflows[instruction["next"]]
                    break
                elif instruction["operator"] == "Accepted":
                    found = True
                    s += part['x'] + part['m'] + part['a'] + part['s']
                    break
                elif instruction["operator"] == "Rejected":
                    found = True
                    break
                elif instruction["operator"] == '<':
                    if part[instruction["category"]] < instruction["value"]:
                        current = workflows[instruction["next"]]
                        break
                elif instruction["operator"] == '>':
                    if part[instruction["category"]] > instruction["value"]:
                        current = workflows[instruction["next"]]
                        break
            if found:
                break
    return s

def compute_best_part(workflows, curr_workflow, part):
    s = 0
    for instruction in curr_workflow:
        if not instruction["operator"]:
            s += compute_best_part(workflows, workflows[instruction["next"]], part)
        elif instruction["operator"] == "Accepted":
            s += ((part['x'][1] - part['x'][0] + 1)
                    * (part['m'][1] - part['m'][0] + 1)
                    * (part['a'][1] - part['a'][0] + 1)
                    * (part['s'][1] - part['s'][0] + 1))
            return s
        elif instruction["operator"] == "Rejected":
            return s
        elif instruction["operator"] == '<':
            new_part = part.copy()
            new_part[instruction["category"]] = (part[instruction["category"]][0], instruction["value"] - 1)
            part[instruction["category"]] = (instruction["value"], part[instruction["category"]][1])
            s += compute_best_part(workflows, workflows[instruction["next"]], new_part)
        elif instruction["operator"] == '>':
            new_part = part.copy()
            new_part[instruction["category"]] = (instruction["value"] + 1, part[instruction["category"]][1])
            part[instruction["category"]] = (part[instruction["category"]][0], instruction["value"])
            s += compute_best_part(workflows, workflows[instruction["next"]], new_part)
    return s

def part_two(workflows):
    init_part = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    return compute_best_part(workflows, workflows["in"], init_part)


if __name__ == "__main__":
    input_path = "./day_19/input.txt"
    workflows, parts = parse_input(input_path)
    print("---Part One---")
    print(part_one(workflows, parts))

    print("---Part Two---")
    print(part_two(workflows))