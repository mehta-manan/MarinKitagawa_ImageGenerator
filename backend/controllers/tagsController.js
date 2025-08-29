const HttpError = require("../utils/HttpError");
const mongoose = require("mongoose");

const getAllTags = async (req, res) => {
  try {
    const tagTypes = [
      "accessories",
      "background_setting",
      "character",
      "clothes_outfits",
      "eyes_expression",
      "focus_bodyParts",
      "hair",
      "headwear_extras",
      "objects_props",
      "pose_body",
      "objects_props",
      "style_themes"
    ];

    let allTags = {};

    const db = mongoose.connection.db;

    for (const tagType of tagTypes) {
      const tags = await db
        .collection(tagType)
        .find({}, { projection: { _id: 0, label: 1, value: 1 } })
        .toArray();

      allTags[tagType] = tags;
    }

    res.status(200).json({status: 200, message: "Tags fetched successfully", tags: allTags });
  } catch (error) {
    throw new HttpError("Fetching tags failed", 500);
  }
};

exports.getAllTags = getAllTags;
