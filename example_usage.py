from client import FormatConverter

alpaca = {"id": "1", "instruction": "Translate to Spanish", "input": "Hello", "output": "Hola"}
sgpt = FormatConverter.alpaca_to_sharegpt(alpaca)
print("ShareGPT conversion:\n", sgpt)
back = FormatConverter.sharegpt_to_alpaca(sgpt)
print("Back to Alpaca:\n", back)
