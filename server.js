const express = require("express");
const path = require("path");

const app = express();

app.use("/assets", express.static(path.resolve(__dirname, "frontend", "assets")));
app.use("/css", express.static(path.resolve(__dirname, "frontend", "css")));
app.use("/js", express.static(path.resolve(__dirname, "frontend", "js")));
app.get("/*", (req, res) => {
    res.sendFile(path.resolve(__dirname, "frontend", "index.html"));
});

app.listen(process.env.PORT || 8081, () => console.log("Server running..."));
