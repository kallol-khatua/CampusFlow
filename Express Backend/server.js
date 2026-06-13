require("dotenv").config();
const express = require("express");
const { google } = require("googleapis");

const app = express();

const oauth2Client = new google.auth.OAuth2(
    process.env.CLIENT_ID,
    process.env.CLIENT_SECRET,
    process.env.REDIRECT_URI
);

// Generate Google login URL
app.get("/auth/google", (req, res) => {

    const url = oauth2Client.generateAuthUrl({
        access_type: "offline",
        scope: [
            "https://www.googleapis.com/auth/gmail.readonly"
        ]
    });

    res.redirect(url);
});


// Callback after user grants permission
app.get("/auth/google/callback", async (req, res) => {

    const code = req.query.code;

    try {

        const { tokens } = await oauth2Client.getToken(code);

        oauth2Client.setCredentials(tokens);

        const gmail = google.gmail({
            version: "v1",
            auth: oauth2Client
        });

        // Get list of emails
        const response = await gmail.users.messages.list({
            userId: "me",
            maxResults: 10
        });

        const messages = response.data.messages;

        let emailList = [];

        for (const msg of messages) {

            const email = await gmail.users.messages.get({
                userId: "me",
                id: msg.id
            });

            const headers = email.data.payload.headers;

            const subject =
                headers.find(h => h.name === "Subject")?.value;

            const from =
                headers.find(h => h.name === "From")?.value;

            emailList.push({
                from,
                subject
            });
        }

        res.json(emailList);

    } catch (err) {

        console.log(err);

        res.status(500).send("Error fetching emails");
    }

});

app.listen(5000, () => {
    console.log("Server running on port 5000");
});