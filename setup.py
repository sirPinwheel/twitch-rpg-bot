from pip._internal import main as p

required_modules = [
    "certifi"
]

for module in required_modules:
    p(['install', module])