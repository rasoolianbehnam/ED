import base64

code = "Zg6afPNqbaMv2WmYFOv57zCU1O6KtrMMdskcmllbZcY4q6t0PrMywqO82PR6AgtfIJhtBABhomNUW2dITwuLfOZuhXILp7Toya+AvWaYJxpfY1lj4ci4cnJxiuUZTev1WV31p5bcwzRM1Cmn3QOCezNNqenhzZD8TZUnOL"
print len(code)

d = len(code) // 16

print base64.b64decode(code[:d*16])
