// This file is used to bundle up Short Stuff for inclusion in the browser as a normal
// script file. This allows it to be used in legacy frontend systems where npm modules
// aren't easily included. For example, in the Django admin.
//
// To prevent its functions from clobbering anything,
// we import them all into an object named shortStuff,
// which is reasonably unlikely to be reserved already.

const shortStuff = require('./dist/index.js')

window.shortStuff = shortStuff
