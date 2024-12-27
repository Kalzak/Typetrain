var express = require('express');
var cors = require('cors');
var bodyParser = require('body-parser');
var app = express();

const { process_race } = require("./race/process_race")

app.use(bodyParser.json());
app.use(cors({
  origin: 'http://localhost:3000', // Allow requests from this origin
  methods: 'GET,POST,PUT,DELETE,OPTIONS', // Allow these methods
  allowedHeaders: 'Content-Type,Authorization', // Allow these headers
}));


app.post("/submitrace", function(req, res) {
  console.log("hello", req.body);
  race_data = req.body;

  let result = process_race(race_data);
  console.log(result);

  res.status(200).send(result);
})

app.listen(4000);
