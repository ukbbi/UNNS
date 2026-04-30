const puppeteer = require('puppeteer');
const readline = require('readline');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    await page.goto('file://' + __dirname + '/struc_perc_i_v2_4_0.html');

    console.log("READY");

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        terminal: false
    });

    rl.on('line', async (line) => {
        try {
            const request = JSON.parse(line);

            const result = await page.evaluate((ladder) => {
                return window.runAnalysisFromData(ladder);
            }, request.ladder);

            console.log(JSON.stringify(result));
        } catch (err) {
            console.error(JSON.stringify({ error: err.toString() }));
        }
    });
})();