"""Macstodon - a Mastodon client for classic Mac OSMIT LicenseCopyright (c) 2022-2023 Scott Small and ContributorsPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associateddocumentation files (the "Software"), to deal in the Software without restriction, including without limitation therights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permitpersons to whom the Software is furnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included in all copies or substantial portions of theSoftware.THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THEWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS ORCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OROTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""# ############### Python Imports # ##############import Imageimport GifImagePluginimport JpegImagePluginimport PngImagePluginimport osimport stringimport sysimport urllib# #################### Third-Party Imports# ###################from third_party.PixMapWrapper import PixMapWrapper# ########### My Imports# ##########from MacstodonHelpers import dprint, getFilenameFromURL# ############ Application# ###########class ImageHandler:    def __init__(self, app):        """        Initializes the ImageHandler class.        """        self.app = app    def getImageFromURL(self, url, cache=None):        """        Wrapper function - given an image URL, either downloads and caches        the image, or loads it from the cache if it already exists there.        """        try:            if cache:                dprint("Want to cache image: %s" % cache)                file_name = getFilenameFromURL(url)                if not self.isCached(file_name, cache):                    dprint("Image is not cached, downloading: %s" % cache)                    self.downloadImage(url, file_name, cache)                    dprint("Resizing image: %s" % cache)                    img = self.resizeAndGetImage(file_name, cache)                else:                    dprint("Image is already cached: %s" % cache)                    img = self.getImageFromCache(file_name, cache)            else:                dprint("Do not want to cache image")                temp_path = self.downloadImage(url)                img = self.resizeAndGetImage(temp_path)                urllib.urlcleanup()            return img        except:            etype, evalue = sys.exc_info()[:2]            dprint("Error loading image: %s: %s" % (etype, evalue))            return None    def isCached(self, file_name, cache):        """        Checks if an image exists in cache or not and returns true/false.        """        if cache == "account" or cache == "banner":            cachepath = self.app.cacheacctfolderpath        elif cache == "media":            cachepath = self.app.cachemediafolderpath        try:            os.stat(os.path.join(cachepath, file_name))            return 1        except:            exc_info = sys.exc_info()            if str(exc_info[0]) == "mac.error" and exc_info[1][0] == 2:                return 0            raise    def getImageFromCache(self, file_name, cache):        """        Loads an image file from the cache.        """        pm = PixMapWrapper()        if cache == "account" or cache == "banner":            file_path = os.path.join(self.app.cacheacctfolderpath, file_name)        elif cache == "media":            file_path = os.path.join(self.app.cachemediafolderpath, file_name)        pil_image = Image.open(file_path)        pm.fromImage(pil_image)        del pil_image        return pm    def downloadImage(self, url, file_name=None, cache=None):        """        Downloads an image from the given URL and writes it to the cache.        """        http_url = string.replace(url, "https://", "http://")        if cache == "account" or cache == "banner":            file_path = os.path.join(self.app.cacheacctfolderpath, file_name)            urllib.urlretrieve(http_url, file_path)        elif cache == "media":            file_path = os.path.join(self.app.cachemediafolderpath, file_name)            urllib.urlretrieve(http_url, file_path)        else:            file_path = None            dest_path, headers = urllib.urlretrieve(http_url)            return dest_path    def resizeAndGetImage(self, file_name, cache=None):        """        Resizes an image to an appropriate size and overwrites the existing cached image.        """        if cache == "account" or cache == "banner":            file_path = os.path.join(self.app.cacheacctfolderpath, file_name)        elif cache == "media":            file_path = os.path.join(self.app.cachemediafolderpath, file_name)        else:            file_path = file_name        pil_image = Image.open(file_path)        pm = PixMapWrapper()        if cache == "account":            pil_image_small = pil_image.resize((48, 48))            del pil_image            pil_image_small.save(file_path)            pm.fromImage(pil_image_small)            del pil_image_small        elif cache == "banner":            pil_image_small = pil_image.resize((384, 128))            del pil_image            pil_image_small.save(file_path)            pm.fromImage(pil_image_small)            del pil_image_small        else:            pm.fromImage(pil_image)            del pil_image        return pm