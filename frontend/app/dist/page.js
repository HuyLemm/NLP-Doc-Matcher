// Page.tsx
"use client";
"use strict";
exports.__esModule = true;
var react_1 = require("react");
var CrawlSection_1 = require("./CrawlSection");
var UploadExtract_1 = require("./UploadExtract");
var UploadCompare_1 = require("./UploadCompare");
function Page() {
    var _a = react_1.useState(null), mode = _a[0], setMode = _a[1]; // 1 = crawl, 2 = extract, 3 = compare
    var _b = react_1.useState(""), message = _b[0], setMessage = _b[1];
    return (React.createElement("div", { className: "container" },
        React.createElement("div", { className: "w-full max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-lg" },
            React.createElement("h1", { className: "text-3xl font-bold text-center text-blue-600 mb-6" }, "\uD83D\uDCCA H\u1EC7 Th\u1ED1ng X\u1EED L\u00FD V\u0103n B\u1EA3n"),
            React.createElement("div", { className: "mb-6 flex justify-center gap-4" },
                React.createElement("button", { onClick: function () { return setMode(1); }, className: "px-4 py-2 rounded-lg font-semibold border " + (mode === 1
                        ? "bg-blue-500 text-white"
                        : "bg-white text-blue-500 border-blue-500") }, "\uD83D\uDE80 Crawl b\u00E1o"),
                React.createElement("button", { onClick: function () { return setMode(2); }, className: "px-4 py-2 rounded-lg font-semibold border " + (mode === 2
                        ? "bg-green-500 text-white"
                        : "bg-white text-green-500 border-green-500") }, "\uD83D\uDCE4 Upload & Extract"),
                React.createElement("button", { onClick: function () { return setMode(3); }, className: "px-4 py-2 rounded-lg font-semibold border " + (mode === 3
                        ? "bg-purple-500 text-white"
                        : "bg-white text-purple-500 border-purple-500") }, "\uD83D\uDD0D Upload & So S\u00E1nh")),
            mode === 1 && React.createElement(CrawlSection_1["default"], { setMessage: setMessage }),
            mode === 2 && React.createElement(UploadExtract_1["default"], null),
            mode === 3 && React.createElement(UploadCompare_1["default"], null),
            message && (React.createElement("p", { className: "text-green-600 text-center mt-4 font-medium" },
                "\u2705 ",
                message)))));
}
exports["default"] = Page;
