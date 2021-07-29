#!/bin/env python

import argparse

from src import fonts_sampler


parser = argparse.ArgumentParser()
parser.add_argument("--clean", action='store_true', required=False)
parser.add_argument("--build", action='store_true', required=False)
parser.add_argument("--run", action='store_true', required=False)
stdin = parser.parse_args()

print("> Application Management")
if(stdin.clean):
	print("Application: Cleaning Environment")
	fonts_sampler.clean(stdin)
elif(stdin.build):
	print("Application: Building Environment")
	fonts_sampler.build(stdin)
elif(stdin.run):
	print("Application: Running Webserver")
	fonts_sampler.run(stdin)
else:
	print("Application: No arguments specified")
	pass