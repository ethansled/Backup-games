const express = require("express");
const ejs = require("ejs");
const ContainerManager = require("./containers");

const app = new express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.set("view engine", "ejs");
app.use("/public", express.static(__dirname + "/public"));

app.get("/", (req, res) => {
    res.render("../public/views/index.ejs");
});

app.get("/games/:appId", (req, res) => {
    console.log(`request for app ${req.params.appId}`)
    res.render("../public/views/game-view.ejs", { frameSource: `http://localhost:8080/${req.params.appId}` })
})

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => console.log(`Server is Running on ${PORT}`));