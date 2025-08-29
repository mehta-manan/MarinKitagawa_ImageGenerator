const mongoose = require("mongoose");

const connectToMongoDB = async () => {
  try {
    const connection = await mongoose.connect(
     `mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASSWORD}@mongo-cluster.wjtgqic.mongodb.net/${process.env.DB_NAME}?retryWrites=true&w=majority&appName=Mongo-Cluster`
    );
    console.log(`MongoDB connected: ${connection.connection.host}:${connection.connection.port}`);
  } catch (error) {
    throw error;
  }
};

module.exports = connectToMongoDB;
