import requests as req
from clint.textui import progress
import progressbar

size = 9080472

url = "https://files1.mp3slash.xyz/stream/a0fc6e4144b1cf3bb86fa65e84d0db23"

wid = [progressbar.AdaptiveTransferSpeed(),progressbar.Timer(),progressbar.Bar(),progressbar.ETA()]
bar = progressbar.ProgressBar(max_value=size, widgets=wid)
t = 0
tracker = range(0,size, 1024)
tracker.append(size)

print("Asking for response")
resp =req.get(url, stream=True)

if 'filename' in resp.headers['Content-Disposition']:
    filename = str(resp.headers['Content-Disposition']).split('filename=')[1].replace(' ', '_')
    print(filename)

print("Downloading {}".format(filename))
with open("{}.mp3".format(filename), 'wb') as file:
    for chunk in resp.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            file.flush()
            t = t+1
            bar.update(tracker[t])
print("Done")