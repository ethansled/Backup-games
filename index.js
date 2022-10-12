const express = require("express");

const ejs = require("ejs");

const app = new express();

app.use(express.json());
app.use(express.urlencoded({extended: true}));

app.set("view engine","ejs");
app.use("/public", express.static(__dirname + "/public"));

app.get("/" , (req,res) => {
    res.render("index");
});

app.get("/number-guess" , function(req,res) {
    res.render("../views/number-guess.ejs");
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => console.log(`Server is Running on ${PORT}`));