"use client";
"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var react_1 = require("react");
var axios_1 = require("axios");
var react_dropzone_1 = require("react-dropzone");
function UploadCompare() {
    var _this = this;
    var _a = react_1.useState(null), file = _a[0], setFile = _a[1];
    var _b = react_1.useState([]), results = _b[0], setResults = _b[1];
    var _c = react_1.useState(false), loading = _c[0], setLoading = _c[1];
    var _d = react_1.useState(null), message = _d[0], setMessage = _d[1];
    var _e = react_dropzone_1.useDropzone({
        accept: {
            "application/pdf": [".pdf"],
            "application/msword": [".doc", ".docx"],
            "application/vnd.ms-excel": [".xls", ".xlsx"]
        },
        multiple: false,
        onDrop: function (acceptedFiles) {
            if (acceptedFiles.length > 0) {
                setFile(acceptedFiles[0]);
                setResults([]);
                setMessage(null);
            }
        }
    }), getRootProps = _e.getRootProps, getInputProps = _e.getInputProps;
    var handleCompare = function () { return __awaiter(_this, void 0, void 0, function () {
        var formData, res, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!file)
                        return [2 /*return*/, alert("⚠ Vui lòng chọn file!")];
                    formData = new FormData();
                    formData.append("file", file);
                    setLoading(true);
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, 4, 5]);
                    return [4 /*yield*/, axios_1["default"].post("http://127.0.0.1:8000/api/compare/", formData, {
                            headers: { "Content-Type": "multipart/form-data" }
                        })];
                case 2:
                    res = _a.sent();
                    setResults(res.data.results || []);
                    setMessage(res.data.message || "✅ So sánh hoàn tất!");
                    return [3 /*break*/, 5];
                case 3:
                    error_1 = _a.sent();
                    setMessage("❌ Lỗi khi so sánh với cơ sở dữ liệu.");
                    return [3 /*break*/, 5];
                case 4:
                    setLoading(false);
                    return [7 /*endfinally*/];
                case 5: return [2 /*return*/];
            }
        });
    }); };
    return (React.createElement("div", { className: "mt-4" },
        React.createElement("div", __assign({}, getRootProps(), { className: "p-4 border-2 border-dashed border-gray-400 text-gray-600 bg-gray-50 text-center rounded-lg cursor-pointer hover:bg-gray-100 transition" }),
            React.createElement("input", __assign({}, getInputProps())),
            React.createElement("p", null, "\uD83D\uDCC2 K\u00E9o & th\u1EA3 file v\u00E0o \u0111\u00E2y ho\u1EB7c b\u1EA5m \u0111\u1EC3 ch\u1ECDn")),
        file && (React.createElement("div", { className: "mt-4 flex items-center justify-between bg-gray-100 p-3 rounded shadow" },
            React.createElement("span", { className: "text-sm text-gray-700" },
                "\uD83D\uDCC4 \u0110\u00E3 ch\u1ECDn: ",
                React.createElement("strong", null, file.name)),
            React.createElement("button", { onClick: function () {
                    setFile(null);
                    setResults([]);
                    setMessage(null);
                }, className: "ml-4 px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600" }, "\u274C G\u1EE1 file"))),
        React.createElement("button", { onClick: handleCompare, disabled: !file || loading, className: "w-full px-4 py-2 mt-4 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition" }, loading ? "🔍 Đang so sánh..." : "🔍 So Sánh File"),
        message && (React.createElement("p", { className: "mt-4 text-center text-blue-600 font-semibold" }, message)),
        results.length > 0 && (React.createElement("div", { className: "mt-6" },
            React.createElement("h3", { className: "text-lg font-bold mb-2 text-gray-800 text-center" },
                "\uD83D\uDCCB Top ",
                results.length,
                " v\u0103n b\u1EA3n t\u01B0\u01A1ng t\u1EF1 nh\u1EA5t:"),
            React.createElement("ul", { className: "space-y-4" }, results.map(function (item, idx) { return (React.createElement("li", { key: idx, className: "bg-gray-100 p-4 rounded shadow-sm border-l-4 border-purple-500" },
                React.createElement("p", { className: "text-sm text-gray-800" },
                    React.createElement("strong", null, "\uD83D\uDCCC Ngu\u1ED3n:"),
                    " ",
                    item.source),
                React.createElement("p", { className: "text-sm text-gray-800" },
                    React.createElement("strong", null, "\uD83D\uDDC2 Chuy\u00EAn m\u1EE5c:"),
                    " ",
                    item.category),
                React.createElement("p", { className: "text-sm text-gray-800" },
                    React.createElement("strong", null, "\uD83D\uDCC8 Similarity:"),
                    " ",
                    React.createElement("span", { className: "text-purple-600 font-semibold" },
                        (item.similarity * 100).toFixed(2),
                        "%")),
                React.createElement("p", { className: "text-sm text-gray-700 mt-2 line-clamp-3" },
                    React.createElement("strong", null, "\uD83D\uDCDD N\u1ED9i dung:"),
                    " ",
                    item.text))); }))))));
}
exports["default"] = UploadCompare;
