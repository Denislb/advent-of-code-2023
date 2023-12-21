from collections import deque
import math

class Module:
    def __init__(self, name):
        self.outputs = []
        self.modules = []
        self.status = False
        self.pulses = deque()
        self.inputs = {}
        self.name = name

    # def __str__(self):
    #     return self.name

    def setOutputs(self, outputs):
        self.outputs = outputs

    def setInputs(self, inputs):
        self.inputs = inputs

    def getStatus(self):
        return self.status

    def computePulses(self):
        for output in self.outputs:
            output.addPulse(self.status, self)
        return True, 0, len(self.outputs)

    def addPulse(self, pulse, parent):
        self.pulses.append(pulse)
class Output(Module):
    def computePulses(self):
        return False, 0, 0

class FlipFlop(Module):
    def computePulses(self):
        if(self.pulses):
            pulse = self.pulses.popleft()
            if not pulse:
                self.status = not self.status
                for output in self.outputs:
                    output.addPulse(self.status, self)
                if self.status == False:
                    return True, 0, len(self.outputs)
                return True, len(self.outputs), 0
        return False, 0, 0

class Conjunction(Module):
    def addPulse(self, pulse, parent):
        self.inputs[parent] = pulse

    def computePulses(self):
        pulse = True
        if all(self.inputs[ipt] == True for ipt in self.inputs):
            pulse = False
        self.status = pulse
        for output in self.outputs:
            output.addPulse(pulse, self)
        if pulse == False:
            return True, 0, len(self.outputs)
        return True, len(self.outputs), 0

def parse_input(filename):
    modules = {}
    outputs = {}
    inputs = {}
    with open(filename) as f:
        for line in f:
            operator, dest = line.strip().split(" -> ")
            op = None
            if operator == "broadcaster":
                modules[operator] = Module(operator)
                op = operator
                inputs[op] = []
            elif operator[0] == "%":
                modules[operator[1:]] = FlipFlop(operator[1:])
                op = operator[1:]
            elif operator[0] == "&":
                modules[operator[1:]] = Conjunction(operator[1:])
                op = operator[1:]
            outputs[op] = dest.split(', ')
            for d in outputs[op]:
                if d not in inputs:
                    inputs[d] = [op]
                else:
                    inputs[d].append(op)

    output_module = None
    for module in modules:
        otp = []
        ipt = {}
        for m in outputs[module]:
            if m not in modules:
                output_module = Output(m)
                otp.append(output_module)
            else:
                otp.append(modules[m])
        for m in inputs[module]:
            ipt[modules[m]] = False
        modules[module].setOutputs(otp)
        modules[module].setInputs(ipt)
    
    ipt = {}
    for m in inputs[output_module.name]:
        ipt[modules[m]] = False
    output_module.setInputs(ipt)
    return modules["broadcaster"], output_module

def compute_pulses(modules):
    high, low = 0, 1
    while modules:
        module = modules.popleft()
        status, r_high, r_low = module.computePulses()
        high += r_high
        low += r_low
        if status:
            for m in module.outputs:
                modules.append(m)
    return high, low


def part_one(broadcaster):
    modules = deque()
    
    total_high, total_low = 0, 0
    for i in range(1000):
        modules.append(broadcaster)
        r_h, r_l = compute_pulses(modules)
        total_high += r_h
        total_low += r_l

    return total_high * total_low

def part_two(broadcaster, output_module):
    modules = deque()

    modules_at_false = {}
    for ipt in output_module.inputs:
        for i in ipt.inputs:
            modules_at_false[i] = set()

    for t in range(10000):
        modules.append(broadcaster)
        while modules:
            module = modules.popleft()
            status, r_high, r_low = module.computePulses()
            if status:
                for m in module.outputs:
                    modules.append(m)
            for m in modules_at_false:
                if m.getStatus() == True:
                    if t not in modules_at_false[m]:
                        modules_at_false[m].add(t)

    ret = []
    for m in modules_at_false:
        ret.append(abs(list(modules_at_false[m])[0] - list(modules_at_false[m])[1]))
    print(ret) # 4019, 3923, 3821, 3919
    return 0
    #return math.lcm(*ret)


if __name__ == "__main__":
    input_path = "./day_20/input.txt"
    broadcaster, output_module = parse_input(input_path)
    print("---Part One---")
    print(part_one(broadcaster))

    print("---Part Two---")
    print(part_two(broadcaster, output_module))