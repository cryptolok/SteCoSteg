# SteCoSteg
Steath Colors Steganography

SteCoSteg is OutGuess successor and Vernam cipher analog in steganography.

Properties:
* plausible deniability
* tampering/jamming resistance
* detection/rubberhose resistance
* compatibility/portability
* white-box
* key recovery/uniqueness
* one-way/irreversibility

Dependencies:
* **Python** - main code, version 2 and 3 compatible
	- PIL - imaging library

Limitations:
* images-only as decoy
* not optimized for big files
* relatively big key size

## How it works

SteCoSteg operates images, JPEGs are used as a decoy. Then, it takes a file and hides it in the image, converting it to PNG, by giving a unique key for the file's retrieval. To unconceal a file in a PNG image, one must specify this key.

The key it-self is just an encoded pixels list that contains the file.

So, SteCoSteg takes a file, decomposes it by bytes, and store these bytes in pixels of an image. The security is achieved by the determination of what pixel to use as a storage and by applying a one-way function.

At this point, it does exactly the same thing as OutGuess, but differently.

The technique is to find the pixels that are more entropic than the others, which basically means to find the least used colors and modify them irreversibly.

Just like Vernam cipher and OutGuess, if SteCoSteg is well used, it will be mathematically impossible to extract the concealed information. This usage requires a highly entropic image (as photo) and relatively small amount of data to store. Bigger amount of storage is possible to conceal as well, but the more data is to be concealed, less stealthy it will be, thus it is not optimized for big amount of data concealement since, the respective decoy size is needed.

The variant of this technique can be used to achieve theoretic-level security with an arbitrary storage length,  by creating customized images with a specific set of colors. However, the variant will produce a result that may draw suspicion, thus unpractical for most cases, regardless the fact that it is truly white-box and can be done in an untrusted environment, without any particular tools. Also, this variant  is one of the (perhaps the) best-one that could exist in steganography because, it uses maximum data space (length) without any special compression or encoding, contrary to the other hiding techniques. The following implementation provides less secure and less universal method, but more practical without significant drawbacks.

## Analysis

It follows the Kerckhoffs's principle, meaning that this is white-box type steganography and all the security is not in the secrecy of the algorithm, but in the key, which is in contrast to security by obscurity, commonly used in steganography.

It combats statistical analysis like LSB enhancement, pixel evaluation, Chi-Square and all sorts of histograms.

Plus, it can resist LSB jamming, the message will be modified, but can be recovered without much effort. Though, if some encryption is used (like AES in CBC mode) jamming may be problematic to recover the message. Anyway, it might be logical to jam some suspicious files, but the point of SteCoSteg is to make the file as innocent as possible and jamming all the images of the entire internet is not realistic, for now.

Like was mentioned, it is possible and even better to encrypt the original message before using steganography, regardless the fact that the following implementation doesn't require encryption to maintain its security, which makes it a cryptography alternative to maintain confidentiality.

All this makes it very viable in extremely restricted conditions, even if the encryption will be banned and everything will be monitored every time, which makes it a valid solution for post-cypherpunk era.

Just like OutGuess, this technique can be applied to any sort of data, but the current implementation is adapted only for JPEG and PNG images, although the other formats are compatible. The main disadvantage is that the implementation doesn't determine the "stealth limit" for a given decoy, but it can be visually determined.

The key is recoverable with the original decoy image and the stealthed-one. However, it is designed to be a time/resource consuming process and without the original decoy image, recovery is impossible. The key is unique per image, which means that it is possible to store different files in one image with the same key.

The code is commented and explained.

### HowTo

For Unix:
```bash
sudo apt-get install python python-pil || echo 'use an appropriate package manager'
python SteCoSteg.py
```
For Windows, [Python](https://www.python.org/downloads/) with [PIL](http://www.pythonware.com/products/pil/). Portable versions are not known to be functional.


To stealth a file:

1. Specify a JPEG image as a decoy

2. Specify a file to stealth

3. Retreive the output PNG image and the respective key


To unstealth a file:

1. Specify a PNG image as a decoy

2. Specify an output file

3. Specify a key or the original JPEG image

4. Retrieve the original file

#### Notes

This is just an implementation of a technology. Further improvement is possible.

Mass surveillance and world control would never be possible.

> "Some tourists think Amsterdam is a city of sin, but in truth it is a city of freedom. And in freedom, most people find sin."

John Green, *The Fault in Our Stars*

