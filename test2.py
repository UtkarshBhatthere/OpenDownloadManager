size = 9080472

url = "https://files1.mp3slash.xyz/stream/a0fc6e4144b1cf3bb86fa65e84d0db23"
fileName = url.split('/')[-1]
path = "/home/utkarshbhatt/folder/"

with open('{}{}.mp3'.format(path,fileName), 'ab') as file:
    for i in range(1,11):
        ftemp = "{}{}.part{}".format(path,fileName, i)
        with open(ftemp, 'rb') as tempfile:
            file.write(tempfile.read())
            file.flush()
            tempfile.close()
