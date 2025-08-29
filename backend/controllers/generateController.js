const HttpError = require("../utils/HttpError");
const { spawn } = require("child_process");
const sendEmail = require("../utils/sendEmail");
const isValidEmail = require("../utils/validations/validations");

const scriptPath = "./ComfyUI/scripts/marin_kitagawa_API.py";

const generateImage = async (req, res, next) => {
  const { email, tags } = req.body;
  
  if (!email) {
    throw new HttpError("Email is required", 400);
  }

  if (!isValidEmail(email)) {
    throw new HttpError("Invalid email format", 400);
  }

  const promptText = "marin_kitagwa1, marin1, kitagawa1, 1girl " + tags;

  try {
    console.log("[NODE] Incoming request with tags:", tags);
    console.log("[NODE] Sending immediate response to client...");

    res.status(200).json({
      status: 200,
      message: `Your request has been received. The image will be emailed to ${email} shortly.`,
    });

    console.log("[NODE] Spawning Python process...");
    const python = spawn("python", [scriptPath, promptText]);

    let data = "";
    python.stdout.on("data", (chunk) => {
      const text = chunk.toString();
      console.log("[PYTHON STDOUT]", text.trim());
      data += text;
    });

    python.stderr.on("data", (err) => {
      console.error("[PYTHON STDERR]", err.toString());
    });

    python.on("close", async (code) => {
      console.log(`[NODE] Python process closed with code: ${code}`);
      console.log("[NODE] Raw Python output collected:", data);

      try {
        const result = JSON.parse(data);
        console.log("[NODE] Parsed Python result:", result);

        if (result.image) {
          console.log(`[NODE] Sending email with image to ${email}...`);

          await sendEmail({
            to: email,
            subject: "Your generated image is ready!",
            html: `
              <p>Here is your generated image:</p>
              <p><strong>Tags used:</strong> ${tags}</p>
              <img src="cid:genImage" style="max-width:600px; border:1px solid #ddd; border-radius:8px;" />
            `,
            attachments: [
              {
                filename: "generated.png",
                content: Buffer.from(result.image, "base64"),
                cid: "genImage",
              },
            ],
          });

          console.log("[NODE] ✅ Email successfully sent to:", email);
        } else {
          console.error("[NODE] ❌ No image generated:", result.error);
        }
      } catch (err) {
        console.error("[NODE] ❌ Failed to parse Python output:", data);
        console.error("[NODE] Error:", err.message);
      }
    });
  } catch (error) {
    console.error("[NODE] Unexpected error:", error.message);
    next(error);
  }
};

exports.generateImage = generateImage;
