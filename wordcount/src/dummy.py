with open("windows_newline.txt", mode="wb") as file:
    file.write(b"Hello\r\nWorld!")
    # file.write(b"Hello\nWorld!")

with open("windows_newline.txt", mode="rb") as file:
    print(list(file.read()))
