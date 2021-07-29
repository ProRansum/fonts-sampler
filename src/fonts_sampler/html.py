from os import path

class HTML:
	class document: pass
	
	def __init__(self, title="No title"):
		self.document.head = [ f"<title>{ title }</title>" ]
		self.document.tail = []
		self.document.body = []
		self.body = self.Body(self)
		
	def dependencies(self, dep_type=None, src:str=None):
		selects = dict([
			("style", f"<link rel=\"stylesheet\" type=\"text/css\" href=\"{ src }\">"),
			("script", f"<script type=\"text/javascript\" src=\"{ src }\"></script>")
		])
		
		if type(src) is not None:
			self.document.head.extend([selects.get( dep_type )])
					
	def styles(self, value:str=None):
		if type(value) is not None:
			self.document.head.extend([ "".ljust(1, '\t') + f"<style>\n{ value }\n</style>" ])
			
	def scripts(self, value:str=None):
		if type(value) is not None:
			self.document.tail.extend([ "".ljust(1, '\t') + f"<script>\n{ value }\n</script>" ])
	
	class Body:
		def __init__(self, parent):
			self.parent = parent
			
		def text(self, value):
			if type(value) is list:
				self.parent.document.body = value
			else:
				self.parent.document.body = [ value ]
			
		def html(self, value): 
			self.text(value)
			
		def append(self, value):
			if type(value) is list:
				self.parent.document.body.extend(value)
			else:
				self.parent.document.body.append(value)
				
		def prepend(self, value):
			arr = []
			if type(value) is list:
				arr.extend(value)
			else:
				arr.append(value)
			
			self.parent.document.body = arr.extend(self.parent.document.body)
				
		def clear(self):
			self.parent.document.body = []
			
	def compile(self, contents:list=["<h1>Hello World<h1>"], **kwargs):
		html = ["<html>"]
		html.extend( self.document.head )
		html.extend( self.document.body )
		html.extend( self.document.tail )
		html.append("</html>")
		self.document.compiled = "\n".join(html)
	
	def write(self, dir, name):
		with open(path.join(dir, name), "w") as file:
			file.flush()
			file.write(self.document.compiled)
