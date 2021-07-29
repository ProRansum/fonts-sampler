import os
import glob
import re
from shutil import copyfile

PATH = os.path.abspath(os.path.dirname(__file__))
FONTS_DIR = os.path.join("C:\\Windows\\Fonts")
FONT_PATHS = [ (os.path.abspath(f), os.path.basename(f), os.path.splitext(os.path.basename(f))[0]) for f in glob.glob(os.path.join(FONTS_DIR, '*')) if '.ttf' in os.path.splitext(f)[1:] ]

CACHE_DIR = os.path.join(PATH, "dist")
if not os.path.isdir(CACHE_DIR):
	os.mkdir(CACHE_DIR)

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
		with open(os.path.join(dir, name), "w") as file:
			file.flush()
			file.write(self.document.compiled)

html = HTML(title="Font Sample Generator")
html.dependencies("script", "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.js")


html.styles("\n".join( [ "".ljust(2, '\t') + '@font-face { font-family: ' + fn + '; src: url(dist/' + ff + '); }' for (_, ff, fn) in FONT_PATHS] ))
html.styles("\n".join( [ "".ljust(2, '\t') + 'td.font-sample[aria-font="' + fn + '"] { font-family: ' + fn + '; }' for (_, ff, fn) in FONT_PATHS] ))

html.styles("""
	td.font-name { text-transform: capitalize; }
	td.font-sample.capitalize { text-transform: capitalize; }
	td.font-sample.uppercase  { text-transform: uppercase; }
	td.font-sample.lowercase  { text-transform: lowercase; }
""")

html.body.append("""
<div class="prefills">
    <select class="case-type">
        <option value="capitalize">Capitalize</option>
        <option value="uppercase">Uppercase</option>
        <option value="lowercase">Lowercase</option>
    </select>
    <label>Font-size: <input class="font-size" value="16px"></label>
    <label>Sample Text: <input id="sample-text" value="Hello World!"></label>
</div>
""")

table = ["<table>"]
table.extend([
    "".ljust(1, '\t') + "<thead>",
    "".ljust(2, '\t') + "<tr>", 
    "".ljust(3, '\t') + "<th>Name</th>", 
    "".ljust(3, '\t') + "<th>Text</th>", 
    "".ljust(2, '\t') + "</tr>",
    "".ljust(1, '\t') + "</thead>",
    "".ljust(1, '\t') + "<tbody>"
])

for (fontDir, fontFile, fontName) in FONT_PATHS:
	CACHE_FILE = os.path.join(CACHE_DIR, fontFile)
	
	if not os.path.isfile(CACHE_FILE):
		copyfile(fontDir, CACHE_FILE)
		
	table.extend([
		"".ljust(2, '\t') + "<tr>", 
		"".ljust(3, '\t') + f"<td class=\"font-name\">{ fontName }</td>",
		"".ljust(3, '\t') + f"<td class=\"font-sample\" aria-font=\"{ fontName }\" style=\"font-size: 16px;\">Hello World!</td>",
		"".ljust(2, '\t') + "</tr>"
	])

table.extend(["".ljust(1, '\t') + "</tbody>", "</table>"])
html.body.append(table)

html.scripts("""
function delay(t,n){var e=0;return function(){var i=this,u=arguments;clearTimeout(e),e=setTimeout(function(){t.apply(i,u)},n||0)}};
$(".case-type").unbind('change').change(function() {
	let val = this.value;
	$(".font-sample").addClass(val).removeClass(["uppercase", "lowercase", "capitalize"].filter(_=> _ !== val))
});

$("input.font-size").keyup(delay(function() {
	let value = ((!this.value) ? "" : this.value.toString()).match(/[0-9]{1,}/g)[0],
		currSize = (!value) ? 16 : value,
		fontSize = currSize + "px";
		
	this.value = fontSize;
	$(".font-sample").attr("style", "font-size: " + fontSize);
}, 1e3));

$("#sample-text").keyup(delay(function() {
	$(".font-sample").text(this.value);
}, 1e3));
""")

html.compile()
html.write(PATH, "index.html")

"""
<div class="prefills">
    <select class="case-type">
        <option value="uppercase">Uppercase</option>
        <option value="lowercase">Lowercase</option>
        <option value="capitalize">Capitalize</option>
    </select>
    <label>
        Font-size: 
        <input id="font-size" placeholder="12px" readonly>
        <button class="font-size" value="1">+</button>
        <button class="font-size" value="-1">-</button>
    </label>
    <label>
        Sample Text: <input id="sample-text" value="Hello World!" readonly>
    </label>
</div>
"""