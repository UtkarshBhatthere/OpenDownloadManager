import requests as req
from clint.textui import progress

size = 9080472

url = "https://files1.mp3slash.xyz/stream/a0fc6e4144b1cf3bb86fa65e84d0db23"
fileName = url.split('/')[-1]


for i in range(0,9):
    start = i * 1000000
    end = (i+1) * 1000000
    hdr = {'RANGE':'bytes={}-{}'.format(start, end)}
    print(hdr)
    print("Header done")
    resp = req.get(url, headers=hdr, stream=True)
    print("Reqsent")
    print(resp.headers.get('Content-Range'))
    with open("/home/utkarshbhatt/folder/{}.part{}".format(fileName, (i+1)), 'wb') as file:
        for chunk in progress.bar(resp.iter_content(chunk_size=1024), expected_size=((end-start)/1024) + 1):
            if chunk:
                file.write(chunk)
                file.flush()

start = 9000000
end = size -1
hdr = {'RANGE':'bytes={}-{}'.format(start, end)}
print(hdr)
print("Header done")
resp = req.get(url, headers=hdr, stream=True)
print("Reqsent")
print(resp.headers.get('Content-Range'))
with open("/home/utkarshbhatt/folder/{}.part{}".format(fileName, (10)), 'wb') as file:
    for chunk in progress.bar(resp.iter_content(chunk_size=1024), expected_size=((end-start)/1024) + 1):
        if chunk:
            file.write(chunk)
            file.flush()