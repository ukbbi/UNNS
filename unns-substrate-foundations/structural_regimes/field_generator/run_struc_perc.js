const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {

  const inputPath = process.argv[2];
  const outputPath = process.argv[3];

  const ladder = fs.readFileSync(inputPath, 'utf-8')
    .split(/\s+/)
    .map(Number);

  const browser = await puppeteer.launch({
    headless: true
  });

  const page = await browser.newPage();

  const htmlPath = 'file://' + path.resolve(__dirname, 'struc_perc_i_v2_4_0.html');

  await page.goto(htmlPath);

  await page.waitForFunction(() => window.runAnalysisFromData !== undefined);

  const result = await page.evaluate(async (ladder) => {
    return await window.runAnalysisFromData(ladder);
  }, ladder);

  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));

  await browser.close();

})();