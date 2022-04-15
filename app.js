require("dotenv").config();
const express = require("express");
const cors = require("cors");
const app = express();

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Listening to port ${PORT}`);
});
