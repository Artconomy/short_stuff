export PATH := node_modules/.bin:$(PATH)
export SHELL := /usr/bin/env bash
export OS := $(shell uname -s)

.DEFAULT_GOAL := oneshot

install_prereqs:
	npm install -D

build:  # Build the NPM package.
	rm -rvf dist
	cp -a src dist
	cp tsconfig.json dist/
	sed -i -e '/"rootDir"/d' dist/tsconfig.json
	cd dist && npx tsc && cd ..
	rm -rvf dist/__mocks__
	find dist -depth -regex '.*/specs[/]?.*' -delete
	cp package.json README.md ../LICENSE.txt dist/
	mkdir dist/browser/
	# Prepare <script> versions of the library in case someone needs these functions
    # outside of a node build environment, such as for the Django admin.
	npx browserify main.js > dist/browser/short-stuff.js
	npx uglifyjs dist/browser/short-stuff.js > dist/browser/short-stuff.min.js
	# Make this available for the Django admin to use.
	cp dist/browser/short-stuff.js ../short_stuff/static/short_stuff/js/

tarball: build
	cd dist && npm pack

oneshot: install_prereqs build

quality:
	npm run lint

test:
	npm run test

publish: install_prereqs build qa
	cd dist && npm publish --access public

qa: quality test

fix:
	npm run lint:fix
