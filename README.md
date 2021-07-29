# fonts-sampler
A py3 package that allows for you to be able to generate a localized environment to be able to view your entire system font library.

### [tl;dr](#)

```bash
# clone repo
git clone git@github.com:ProRansum/fonts-sampler.git
cd fonts-sampler/
# install dependencies, if needed
python -m pip install -r requirements.txt
# build environmnet and resources 
python manage.py --build 
# run local webserver to resources
# open "http:localhost:8000" in browser if it doesnt open for you.
python manage.py --run
# clean all generations
python manage.py --clean
```

## [Requirements](#)
- Python 2.X/3.X, for setup follow: [Installing Python](#installing-python)


## [How-to Run](#)
1. Change to the repository `cd fonts-sampler/`.
2. Install the dependencies `python -m pip install -r requirements.txt`.
3. `manage.py` is the package manager that handles how to execute the package.
 - __--build__: Generates a cache of system fonts to be served by the webserver, and automatically generates an `index.html` that contains all of the cached fonts.
 - __--run__: Launches a local webserver on port _8000_, all font files can be access under `/fonts/*` under the `dist/` directory.
 - __--clean__: Cleans all files generated during the build process.
4. Enjoy!


## Licence
Copyright (c) 2021, Kevin Haas. All rights reserved.


## Support
If you like my work(s), don't be shy to [buy me a coffee](https://www.buymeacoffee.com/kevinhaas)!


__Drink coffee and hack the planet!__
