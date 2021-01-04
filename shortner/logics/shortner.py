def idToShortURL(id):
    map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    shortURL = ""

    # for each digit find the base 62
    while (id > 0):
        shortURL += map[id % 62]
        id //= 62

    # reversing the shortURL
    return shortURL[len(shortURL):: -1]


def shortURLToId(shortURL):
    id = 0
    for i in shortURL:
        val_i = ord(i)
        if (val_i >= ord('a') and val_i <= ord('z')):
            id = id * 62 + val_i - ord('a')
        elif (val_i >= ord('A') and val_i <= ord('Z')):
            id = id * 62 + val_i - ord('Z') + 26
        else:
            id = id * 62 + val_i - ord('0') + 52
    return id

