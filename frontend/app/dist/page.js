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
function Home() {
    var _this = this;
    var _a = react_1.useState(10), numArticles = _a[0], setNumArticles = _a[1];
    var _b = react_1.useState("tuoitre"), category = _b[0], setCategory = _b[1];
    var _c = react_1.useState(false), loading = _c[0], setLoading = _c[1];
    var _d = react_1.useState(""), message = _d[0], setMessage = _d[1];
    var _e = react_1.useState([]), files = _e[0], setFiles = _e[1];
    var handleCrawl = function () { return __awaiter(_this, void 0, void 0, function () {
        var response, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    setLoading(true);
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, 4, 5]);
                    return [4 /*yield*/, axios_1["default"].get("http://127.0.0.1:8000/api/crawl/" + category + "/?n=" + numArticles)];
                case 2:
                    response = _a.sent();
                    setMessage(response.data.message);
                    return [3 /*break*/, 5];
                case 3:
                    error_1 = _a.sent();
                    setMessage("❌ Có lỗi xảy ra!");
                    return [3 /*break*/, 5];
                case 4:
                    setLoading(false);
                    return [7 /*endfinally*/];
                case 5: return [2 /*return*/];
            }
        });
    }); };
    var _f = react_dropzone_1.useDropzone({
        accept: {
            "application/pdf": [".pdf"],
            "application/msword": [".doc", ".docx"],
            "application/vnd.ms-excel": [".xls", ".xlsx"]
        },
        onDrop: function (acceptedFiles) { return setFiles(acceptedFiles); }
    }), getRootProps = _f.getRootProps, getInputProps = _f.getInputProps;
    var handleUpload = function () { return __awaiter(_this, void 0, void 0, function () {
        var formData, response, error_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (files.length === 0) {
                        alert("⚠ Vui lòng chọn file để tải lên!");
                        return [2 /*return*/];
                    }
                    formData = new FormData();
                    files.forEach(function (file) { return formData.append("file", file); });
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, axios_1["default"].post("http://127.0.0.1:8000/api/upload/", formData, { headers: { "Content-Type": "multipart/form-data" } })];
                case 2:
                    response = _a.sent();
                    alert(response.data.message);
                    return [3 /*break*/, 4];
                case 3:
                    error_2 = _a.sent();
                    alert("❌ Có lỗi xảy ra khi tải lên file!");
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    }); };
    return (React.createElement("div", { className: "container" },
        React.createElement("div", { className: "w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg" },
            React.createElement("h1", { className: "text-3xl font-bold text-center text-blue-600 mb-6" }, "\uD83D\uDCCA Crawl B\u00E0i Vi\u1EBFt & T\u1EA3i L\u00EAn File"),
            React.createElement("div", { className: "mb-4" },
                React.createElement("label", { className: "block text-lg font-medium text-gray-700" }, "\uD83D\uDCC4 S\u1ED1 l\u01B0\u1EE3ng b\u00E0i vi\u1EBFt:"),
                React.createElement("input", { type: "number", value: numArticles, onChange: function (e) { return setNumArticles(Number(e.target.value)); }, className: "w-full p-2 border border-gray-300 rounded mt-1 focus:ring-blue-500 focus:border-blue-500" })),
            React.createElement("div", { className: "mb-4" },
                React.createElement("label", { className: "block text-lg font-medium text-gray-700" }, "\uD83D\uDCF0 Ch\u1ECDn chuy\u00EAn m\u1EE5c:"),
                React.createElement("select", { value: category, onChange: function (e) { return setCategory(e.target.value); }, className: "w-full p-2 border border-gray-300 rounded mt-1 focus:ring-blue-500 focus:border-blue-500" },
                    React.createElement("option", { value: "tuoitre" }, "Tu\u1ED5i Tr\u1EBB"),
                    React.createElement("option", { value: "thanhnien" }, "Thanh Ni\u00EAn"),
                    React.createElement("option", { value: "nld" }, "Ng\u01B0\u1EDDi Lao \u0110\u1ED9ng"),
                    React.createElement("option", { value: "sggp" }, "S\u00E0i G\u00F2n Gi\u1EA3i Ph\u00F3ng"))),
            React.createElement("button", { onClick: handleCrawl, disabled: loading, className: "w-full px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 transition duration-300" }, loading ? "⏳ Đang crawl..." : "🚀 Crawl Dữ Liệu"),
            message && React.createElement("p", { className: "text-green-500 text-center mt-2" }, message),
            React.createElement("div", __assign({}, getRootProps(), { className: "mt-6 p-4 border-2 border-dashed border-gray-400 text-gray-600 bg-gray-50 text-center rounded-lg cursor-pointer hover:bg-gray-100 transition" }),
                React.createElement("input", __assign({}, getInputProps())),
                React.createElement("p", null, "\uD83D\uDCC2 K\u00E9o & th\u1EA3 file v\u00E0o \u0111\u00E2y ho\u1EB7c b\u1EA5m \u0111\u1EC3 ch\u1ECDn file")),
            React.createElement("button", { onClick: handleUpload, className: "w-full px-4 py-2 mt-4 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-300" }, "\uD83D\uDCE4 T\u1EA3i l\u00EAn file"))));
}
exports["default"] = Home;
