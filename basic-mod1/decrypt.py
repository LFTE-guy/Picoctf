set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
with open("message.txt","r") as f:
    numse = f.read().split()

for num in numse:
    r=int(num) % 37
    print(r)
    print(set[r], end='')