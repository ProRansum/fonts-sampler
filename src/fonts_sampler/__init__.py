import re
from os import path, mkdir, makedirs, remove, rmdir
from glob import glob
from shutil import copyfile

from src.fonts_sampler.html import HTML


# Import the needed sub-dir's, if needed 
__all__ = [ path.basename(f)[:3] for f in glob(path.dirname(__file__) + "/*py") 
	if path.isfile(f) and not f.endswith("__init__.py") ]



APP_ROOT = path.abspath(path.dirname(__file__))

FONT_PATHS = [ (path.abspath(f), path.basename(f), path.splitext(path.basename(f))[0]) for f in glob(path.join(path.join("C:\\Windows\\Fonts"), '*')) 
	if '.ttf' in path.splitext(f)[1:] ]

DIST_DIR = path.join("dist")
CACHE_DIR = path.join(DIST_DIR, "fonts")


def build(stdin):
	# create font cache, if it doesn't exist
	if not path.isdir(CACHE_DIR):
		makedirs(CACHE_DIR)
	
	# setup pre-requisites and initialize objects
	html = HTML(title="Font Sample Generator")
	html.dependencies("script", "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.js")
	html.styles("""
		td.font-name { text-transform: capitalize; }
		td.font-sample.capitalize { text-transform: capitalize; }
		td.font-sample.uppercase  { text-transform: uppercase; }
		td.font-sample.lowercase  { text-transform: lowercase; }
	""")
	
	# generating font styles 
	html.styles("\n".join( [ "".ljust(2, '\t') + '@font-face { font-family: ' + fn + '; src: url(fonts/' + ff + '); }' for (_, ff, fn) in FONT_PATHS] ))
	html.styles("\n".join( [ "".ljust(2, '\t') + 'td.font-sample[aria-font="' + fn + '"] { font-family: ' + fn + '; }' for (_, ff, fn) in FONT_PATHS] ))
	
	# all script are pushed to the tail of the body, so this will be 
	# loaded after the document has been loaded.
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
	
	# add the user interactives 
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
	
	# create the head of the table
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
	
	# parse over all fonts cached and create entries to the table 
	# and copy the file from the fonts dir to the target dir 
	# default: './dist/fonts'
	print(f"Caching Fonts [{ CACHE_DIR }].")
	
	for (fontDir, fontFile, fontName) in FONT_PATHS:
		CACHE_FILE = path.join(CACHE_DIR, fontFile)
		
		# copy font file if the file doesn't already exist 
		if not path.isfile(CACHE_FILE):
			copyfile(fontDir, CACHE_FILE)
			
			if path.isfile(CACHE_FILE):
				print(f"   - Caching [{ CACHE_FILE }]. SUCCESS.")
			else:
				print(f"   - Caching [{ CACHE_FILE }]. FAILED.")
		else:
			print(f"   - Cached Already [{ CACHE_FILE }]. Skipped.")

		
		# add new table row for the font
		table.extend([
			"".ljust(2, '\t') + "<tr>", 
			"".ljust(3, '\t') + f"<td class=\"font-name\">{ fontName }</td>",
			"".ljust(3, '\t') + f"<td class=\"font-sample\" aria-font=\"{ fontName }\" style=\"font-size: 16px;\">Hello World!</td>",
			"".ljust(2, '\t') + "</tr>"
		])
		
	# close the tbody and table  
	table.extend(["".ljust(1, '\t') + "</tbody>", "</table>"])
	html.body.append(table)
	
	print("Generating HTML.")
	# compile the html object into an .html file
	html.compile()
	html.write(DIST_DIR, "index.html")
	print(f"HTML generated [{ path.join(DIST_DIR, 'index.html') }]")
	print("Re-run script with flag:'--run' to run a localized server to view the file.")

def clean(stdin):
	
	html_file = path.join(DIST_DIR, "index.html")
	if path.isfile(html_file):
		remove(html_file,)
		print(f"Removed HTML Generated file [{ html_file }].")
	
	# parse over each fonts that are cached and attempt to remove them 
	# from the directory.
	print(f"Cleaning [{ DIST_DIR }].")
	
	if path.isdir(CACHE_DIR):
		for CACHE_FILE in glob(path.join(CACHE_DIR, '*')):
			remove(CACHE_FILE, )
			
			if not path.isfile(CACHE_FILE):
				print(f"Remove [{ CACHE_FILE }]. SUCCESS.")
			else:
				print(f"Remove [{ CACHE_FILE }]. FAILED.")
				
		rmdir(CACHE_DIR,)
		if not path.isdir(CACHE_DIR):
			print(f"Remove [{ CACHE_DIR }]. SUCCESS.")
		else:
			print(f"Remove [{ CACHE_DIR }]. FAILED.")
				
	print("Cleaned")

def run(stdin):
	import webbrowser
	import http.server
	import socketserver
	
	PORT = 8000
	DIRECTORY = DIST_DIR
	
	class Handler(http.server.SimpleHTTPRequestHandler):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, directory=DIRECTORY, **kwargs)
			
	with socketserver.TCPServer(("", PORT), Handler) as httpd:
		print(f"Serving at port: { PORT }")
		webbrowser.open(f'http://localhost:{ PORT }')
		
		httpd.serve_forever()
		server()