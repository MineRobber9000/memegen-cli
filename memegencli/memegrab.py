"""Meme grabber class. AKA the programmatic side of the CLI.

Given a template name, top text, and bottom text, Meme.url is the URL to get said meme.
Meme.download will download said meme.

CustomMeme is a helper class. Instantiated in the same way as Meme, but with a URL instead of template name.
Under the hood, custom memes are of the "custom" template.
"""
import requests
from urllib.parse import quote as quote_raw

def quote(*args):
	"""URL-quote arguments"""
	return quote_raw(*args,safe="")

class Meme:
	"""A meme. Has a template, top text, bottom text, and assorted keyword arguments."""
	def __init__(self,template,top_text,bottom_text,**kwargs):
		self.kwargs = kwargs
		self.template = template
		self.top_text = top_text
		self.bottom_text = bottom_text
		# base_url tag is used for other memegen instances.
		if "base_url" in kwargs:
			self.base_url = kwargs["base_url"]
			del kwargs["base_url"]
		else:
			self.base_url = "https://memegen.link/"
	@property
	def url(self):
		"""URL of the meme."""
		return self.base_url+"{}/{}/{}.jpg".format(self.template,self._escape(self.top_text),self._escape(self.bottom_text))+("?"+"&".join(["{}={}".format(k,quote(self.kwargs[k])) for k in self.kwargs]) if self.kwargs else "")
	def _escape(self,text):
		"""Escapes text in the encoding used by memegen."""
		if not text: return "_"       # escape empty string
		text = text.replace("_","__") # escape underscores
		text = text.replace(" ","_")  # escape spaces
		text = text.replace("-","--") # escape dashes
		text = text.replace("''",'"') # escape double quote
		text = text.replace("?","~q") # escape question marks
		text = text.replace("%","~p") # escape question marks
		text = text.replace("#","~h") # escape question marks
		text = text.replace("/","~s") # escape question marks
		return text
	def download(self,fn):
		"""Will eventually download the meme."""
		return False #TODO: implement meme download

class CustomMeme(Meme):
	"""A meme with a custom background. Same as Meme, but using template `custom`."""
	def __init__(self,url,top,bottom,**kwargs):
		kwargs["alt"]=url
		super(CustomMeme,self).__init__("custom",top,bottom,**kwargs)
