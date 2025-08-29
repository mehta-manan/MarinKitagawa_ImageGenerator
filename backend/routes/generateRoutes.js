const express = require("express");
const router = express.Router();

const generateController = require("../controllers/generateController");

router.post("/", generateController.generateImage);

module.exports = router;