const fs = require('fs');
let code = fs.readFileSync('app.js', 'utf-8');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const html = fs.readFileSync('index.html', 'utf-8');
const dom = new JSDOM(html);
global.window = dom.window;
global.document = dom.window.document;
global.navigator = dom.window.navigator; global.localStorage = { getItem: () => null, setItem: () => {} }; = dom.window.navigator;

try {
    eval(code);
    console.log("APP JS LOADED AND EXECUTED WITHOUT CRASHING!");
} catch (e) {
    console.error(e);
}
