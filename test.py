from headers import headers

dictionary = {key.decode("utf-8"): value.decode("utf-8") for key, value in headers}

print(dictionary)
