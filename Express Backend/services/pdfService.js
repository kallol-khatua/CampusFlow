const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer-core");
const chromium = require("@sparticuz/chromium");

async function generatePDF(email, user) {

    // Create user folder
    const folderPath = path.join(
        __dirname,
        "..",
        "uploads",
        user.email
    );

    if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, {
            recursive: true
        });
    }

    const pdfPath = path.join(
        folderPath,
        `${email.gmailId}.pdf`
    );

    // Skip if PDF already exists
    if (fs.existsSync(pdfPath)) {
        return pdfPath;
    }

    const html = `
    <!DOCTYPE html>
    <html>
    <head>
        <style>

            body{
                font-family: Arial;
                padding:40px;
                line-height:1.5;
            }

            .header{
                border-bottom:1px solid #ccc;
                margin-bottom:20px;
            }

            .body{
                margin-top:30px;
            }

        </style>
    </head>

    <body>

        <div class="header">

            <h2>${email.subject}</h2>

            <p>
                <strong>From:</strong>
                ${email.from}
            </p>

            <p>
                <strong>To:</strong>
                ${email.to}
            </p>

            <p>
                <strong>Date:</strong>
                ${email.date}
            </p>

        </div>

        <div class="body">

            ${email.html}

        </div>

    </body>
    </html>
    `;

    const browser = await puppeteer.launch({
        args: chromium.args,
        defaultViewport: chromium.defaultViewport,
        executablePath: await chromium.executablePath(),
        headless: true
    });

    const page = await browser.newPage();

    await page.setContent(
        html,
        {
            waitUntil: "networkidle0"
        }
    );

    await page.pdf({
        path: pdfPath,
        format: "A4",
        printBackground: true
    });

    await browser.close();

    return pdfPath;

}

module.exports = {
    generatePDF
};