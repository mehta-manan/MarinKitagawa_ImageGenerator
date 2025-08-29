const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const connectToMongoDB = require("./config/db");
const dotenv = require("dotenv");
const homeRoutes = require("./routes/homeRoutes");
const tagRoutes = require("./routes/tagsRoutes");
const generateRoutes = require("./routes/generateRoutes");

dotenv.config();
const app = express();

// ====== MIDDLEWARES ======
app.use(cors());
app.use(express.json());
app.use(bodyParser.json({ limit: "50mb" }));

// Log all incoming requests
app.use((req, res, next) => {
  console.log("[REQUEST]", {
    time: new Date().toISOString(),
    method: req.method,
    path: req.path,
    body: req.body,
  });
  next();
});

// ====== ROUTES ======
app.use("/tags", tagRoutes);
app.use("/generate", generateRoutes);
app.use("/", homeRoutes);

// Not Found handler
app.use((req, res) => {
  console.warn("[404]", {
    time: new Date().toISOString(),
    path: req.path,
    method: req.method,
  });
  res.status(404).json({ status: 404, error: "Not Found" });
});

// Global Error handler
app.use((err, req, res, next) => {
  console.error("[ERROR]", {
    time: new Date().toISOString(),
    path: req.path,
    method: req.method,
    error: err.message,
    stack: err.stack,
  });
  res.status(err.code || 500).json({
    status: err.code || 500,
    message: err.message || "Something went wrong",
  });
});

// ====== START SERVER ======
const PORT = process.env.PORT || 8080;
connectToMongoDB()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`[SERVER] Server started 🚀 Listening on PORT: ${PORT}`);
    });
  })
  .catch((error) => {
    console.error("[MONGO ERROR] MongoDB connection failed:", error.message);
    process.exit(1);
  });
