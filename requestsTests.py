import requests as req

url = "https://files1.mp3slash.xyz/stream/a0fc6e4144b1cf3bb86fa65e84d0db23"
size = 9080472

a = req.get(url, stream=True)
if 'filename' in a.headers['Content-Disposition']:
    filename = str(a.headers['Content-Disposition']).split('filename=')[1].replace(' ', '_')
    print(filename)
