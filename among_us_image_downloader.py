#! python3
# among_us_image_downloader - Downloads every among us images in https://www.citypng.com/.

import requests
import time
import bs4
import os

url = "https://www.citypng.com/search?q=among+us"
os.makedirs('images', exist_ok=True)
page_count = 0

while url != None:

    # Download the page
    print('Downloading page %s...' % url)
    try:
        res = requests.get(url)
        res.raise_for_status()
    except Exception as exc:
        print(exc)
    else:
        print("Status Code: %d" % (res.status_code))
    
    soup = bs4.BeautifulSoup(res.text, "lxml")
    
    # Find the URL of the images.
    img_elems = soup.select('.row img')
    print("Page: %d \nImages: %d" % (page_count, len(img_elems)))
    if img_elems == []:
        print("Could not find any among us images.")
    else:
        # Download the images.
        for img in img_elems:
            img_url = img.get("data-src")
            try:
                res = requests.get(img_url)
                res.raise_for_status()
            except Exception as exc:
                print(exc)
            else:
                print("Status Code: %d" % (res.status_code))
                print("Downloading image %s..." % (img_url))
                # Save the image to .images/.
                img_file = open(os.path.join('images', os.path.basename(img_url)), "wb")
                for chunk in res.iter_content(100000):
                    img_file.write(chunk)
                img_file.close()
            time.sleep(5)
    
    # Get the Next button's url.
    next_link = soup.select('a[rel="next"]')[0]
    url = next_link.get("href")
    page_count = page_count + 1
    time.sleep(15)
    
print('Done.')
