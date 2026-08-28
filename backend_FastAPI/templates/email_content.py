class EmailContentTemplates:
    @staticmethod
    def get_plain_text_email_content(prompt, seed):
        return f"""
🌸 Marin Kitagawa Image Generator 🌸

Hello! 👋

✨ Your image has been successfully generated! 🎨🖼️

━━━━━━━━━━━━━━━━━━━━
🎨 Generation Details
━━━━━━━━━━━━━━━━━━━━

🆔 Prompt ID: {prompt["id"]}

💭 Prompt:
{prompt["text"]}

🎲 Seed: {seed}

━━━━━━━━━━━━━━━━━━━━

📎 Your generated image is attached to this email.

✨ Thank you for using the Marin Kitagawa Image Generator! 💕
We hope you enjoy your generated image! 🌸🖼️

Have a wonderful day! ☀️😊

Best regards,
🌸 Marin Kitagawa Image Generator
🤖 Image Generation Service
"""
    @staticmethod
    def get_html_email_content(prompt, seed):
        return f"""
<h2>🌸 Marin Kitagawa Image Generator 🌸</h2>

<p>Hello! 👋</p>

<p>
    ✨ Your image has been <strong>successfully generated!</strong> 🎨🖼️
</p>

<h3>🎨 Generation Details</h3>

<table style="border-collapse: collapse; width: 100%; max-width: 650px;">
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">
            🆔 <strong>Prompt ID</strong>
        </td>
        <td style="padding: 10px; border: 1px solid #ddd;">
            {prompt["id"]}
        </td>
    </tr>

    <tr>
        <td style="padding: 10px; border: 1px solid #ddd; vertical-align: top;">
            💭 <strong>Prompt</strong>
        </td>
        <td style="padding: 10px; border: 1px solid #ddd;">
            {prompt["text"]}
        </td>
    </tr>

    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">
            🎲 <strong>Seed</strong>
        </td>
        <td style="padding: 10px; border: 1px solid #ddd;">
            {seed}
        </td>
    </tr>
</table>

<p>
    📎 Your generated image is attached to this email.
</p>

<p>
    ✨ Thank you for using the
    <strong>Marin Kitagawa Image Generator</strong>! 💕
</p>

<p>
    We hope you enjoy your generated image! 🌸🖼️✨
</p>

<p>
    Have a wonderful day! ☀️😊🌷
</p>

<p>
    Best regards,<br>
    🌸 <strong>Marin Kitagawa Image Generator</strong><br>
    🤖 Image Generation Service
</p>
"""