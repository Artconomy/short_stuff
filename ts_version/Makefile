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
	cd dist && npx tsc -d && cd ..
	rm -rvf dist/__mocks__
	find dist -regex '.*/specs[/]?.*' -delete
	find dist -regex '.*[.]ts' -not -regex ".*[.]d[.]ts" -delete
	find dist -regex '.*[.]test[.].*' -delete
	rm dist/tsconfig.json
	cp package.json README.md ../LICENSE.txt dist/

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
