const express = require("express");
const ejs = require("ejs");

const ContainerManager = require("./containers.js")

const app = new express();

app.use(express.json());
app.use(express.urlencoded({extended: true}));

app.set("view engine","ejs");
app.use("/public", express.static(__dirname + "/public"));

app.get("/" , (req,res) => {
    res.render("index");
});

app.get("/games/:appId", (req, res) => {
    
})

app.get("/tower-defense" , function(req,res) {
    res.render("../views/tower-defense.ejs");
});

app.get("/retro-racing" , function(req,res) {
    res.render("../views/retro-racing.ejs");
});

app.get("/black-jack" , function(req,res) {
    res.render("../views/black-jack.ejs");
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => console.log(`Server is Running on ${PORT}`));