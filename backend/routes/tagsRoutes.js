const express = require("express");
const router = express.Router();

const tagController = require("../controllers/tagsController");

router.get("/", tagController.getAllTags);

module.exports = router;