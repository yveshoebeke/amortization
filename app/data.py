import math

# App specific data class
class Process:
    principle: float
    roiAmnt: float
    interestRate: float
    investmentTime: float
    duration: dict({"years":float, "months":float})
    result: float

    def __init__(self):
        self.result = 0.0
        self.principle = 0.0
        self.roiAmnt = 0.0
        self.interestRate = 0.0
        self.investmentTime = 0.0
        self.duration = {"years": 0.0, "months": 0.0}
        self.calculators = [self.roiFunc, self.principleFunc, self.rateFunc, self.durationFunc]

    def setParameters(self, p, r, i, d):
        self.principle = p
        self.roiAmnt = r
        self.interestRate = i
        self.investmentTime = d

    def roiFunc(self):
        self.result = self.roiAmnt = self.principle * pow((1 + (self.interestRate / 100)), self.investmentTime)

    def rateFunc(self):
        self.result = self.interestRate = (pow((self.roiAmnt / self.principle), (1 / self.investmentTime)) - 1) * 100

    def principleFunc(self):
        self.result = self.principle = self.roiAmnt / pow((1 + (self.interestRate / 100)), self.investmentTime)

    def durationFunc(self):
        self.result = self.investmentTime = math.log((self.roiAmnt / self.principle), (1 + (self.interestRate / 100)))
        self.duration["months"] = round(round((self.investmentTime % 1), 1) * 12)
        self.duration["years"] = self.investmentTime - (self.investmentTime % 1)
        if self.duration["months"] == 12:
            self.duration["years"] += 1
            self.duration["months"] = 0
