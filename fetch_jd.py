import urllib.request
import re
import os

url = 'https://www.justdial.com/Jamnagar/Gopnath-Mahadev-View-Point-Zinavari/0288PX288-X288-230720033659-C4W7_BZDET'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    img_urls = set(re.findall(r'https://content[0-9]*\.jdmagicbox\.com/[^\s"\'<>]+', html))
    print(f"Found {len(img_urls)} Justdial photos:")
    media_dir = r'c:\gopnath temple\myproject\media'
    
    idx = 1
    for u in img_urls:
        if '.jpg' in u or '.jpeg' in u or '.png' in u:
            try:
                img_data = urllib.request.urlopen(urllib.request.Request(u, headers=headers)).read()
                if len(img_data) > 10000: # filter small icons
                    fname = f'jd_real_photo_{idx}.jpg'
                    dest = os.path.join(media_dir, fname)
                    open(dest, 'wb').write(img_data)
                    print(f"Downloaded real photo {idx}: {fname} ({len(img_data)} bytes) from {u}")
                    idx += 1
            except Exception as e:
                pass
except Exception as e:
    print(f"Error: {e}")
