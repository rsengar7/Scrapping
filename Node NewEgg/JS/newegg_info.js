const fs = require('fs');
const axios = require('axios');
const csvParser = require('csv-parser');
const path = require('path');
const puppeteer = require('puppeteer');
const csvWriter = require('csv-writer').createObjectCsvWriter;

// Read the CSV file to get URLs
const csvFilePath = path.join(__dirname, 'urls.csv');

// Arrays to hold the data
let product_url = [];
let ai_advantages = [];
let ai_disadvantages = [];
let ai_review = [];
let Brandid = [];
let Brand = [];
let shippingCountry = [];
let Price = [];
let product_title = [];
let product_description = [];
let product_imdescription = [];
let product_BulletDescription = [];
let product_LineDescription = [];
let product_WebDescription = [];
let product_ShortTitle = [];
let product_SubcategoryId = [];
let product_sub_category = [];
let product_ItemGroupID = [];
let product_group_num = [];
let product_total_rating = [];

const failed_url = [];

(async () => {
  try {
    // Read CSV and scrape the data
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    const rows = [];
    fs.createReadStream(csvFilePath)
      .pipe(csvParser())
      .on('data', (row) => rows.push(row))
      .on('end', async () => {
        console.log(`Total URLs to scrape: ${rows.length}`);

        for (const row of rows) {
          try {
            const url = row['Url'];
            product_url.push(url);
            const ids = url.split('/').pop().substring(-8);
            let num = '';

            for (let index = 0; index < ids.length; index++) {
              if ([1, 4].includes(index)) {
                num += ids[index] + '-';
              } else {
                num += ids[index];
              }
            }

            const summary_api = `https://www.newegg.com/product/api/getAIReviewSummary?ItemNumber=${num}`;
            const product_api = `https://www.newegg.com/product/api/ProductRealtime?ItemNumber=${num}&RecommendItem=&BestSellerItemList=&IsVATPrice=True`;

            // Make requests to get product data
            const summary_res = await axios.get(summary_api);
            const summary_data = summary_res.data;

            if (summary_data.Data && summary_data.Data.length > 0) {
              const aiContent = summary_data.Data[0]['AIReviewContent'];
              ai_advantages.push(aiContent.Advantages ? aiContent.Advantages.map(a => a.Advantage).join(', ') : '');
              ai_disadvantages.push(aiContent.Disadvantages ? aiContent.Disadvantages.map(d => d.Disadvantage).join(', ') : '');
              ai_review.push(aiContent.Conclusion || '');
            } else {
              ai_advantages.push('');
              ai_disadvantages.push('');
              ai_review.push('');
            }

            const product_res = await axios.get(product_api);
            const product_data = product_res.data.MainItem;
            const description = product_data.Description || {};

            product_description.push(description || '');
            product_title.push(description.Title || '');
            product_imdescription.push(description.IMDescription || '');
            product_BulletDescription.push(description.BulletDescription || '');
            product_LineDescription.push(description.LineDescription || '');
            product_WebDescription.push(description.WebDescription || '');
            product_ShortTitle.push(description.ShortTitle || '');
            product_SubcategoryId.push(product_data.Subcategory?.SubcategoryId || '');
            product_sub_category.push(product_data.Subcategory?.SubcategoryDescription || '');
            product_ItemGroupID.push(product_data.ItemGroupID || '');
            product_group_num.push(product_data.Review?.CombineGroup || '');
            product_total_rating.push(product_data.Review?.HumanRating || '');
            Brandid.push(product_data.ItemManufactory?.BrandId || '');
            Brand.push(product_data.ItemManufactory?.Manufactory || '');
            shippingCountry.push(product_data.ShipFromCountryName || '');
            Price.push(product_data.OriginalUnitPrice || '');

            console.log(`Processed: ${url}`);
          } catch (err) {
            console.log(`Failed to process: ${row['Url']}, Error: ${err.message}`);
            failed_url.push(row['Url']);
          }
        }

        // Create CSV data
        const csvData = {
          Url: product_url,
          ai_advantages,
          ai_disadvantages,
          ai_review,
          Brandid,
          Brand,
          shippingCountry,
          Price,
          product_title,
          product_description,
          product_imdescription,
          product_BulletDescription,
          product_LineDescription,
          product_WebDescription,
          product_ShortTitle,
          product_SubcategoryId,
          product_sub_category,
          product_ItemGroupID,
          product_group_num,
          product_total_rating,
        };

        const records = Object.keys(csvData.Url).map(index => {
          return {
            Url: csvData.Url[index],
            ai_advantages: csvData.ai_advantages[index],
            ai_disadvantages: csvData.ai_disadvantages[index],
            ai_review: csvData.ai_review[index],
            Brandid: csvData.Brandid[index],
            Brand: csvData.Brand[index],
            shippingCountry: csvData.shippingCountry[index],
            Price: csvData.Price[index],
            product_title: csvData.product_title[index],
            product_description: csvData.product_description[index],
            product_imdescription: csvData.product_imdescription[index],
            product_BulletDescription: csvData.product_BulletDescription[index],
            product_LineDescription: csvData.product_LineDescription[index],
            product_WebDescription: csvData.product_WebDescription[index],
            product_ShortTitle: csvData.product_ShortTitle[index],
            product_SubcategoryId: csvData.product_SubcategoryId[index],
            product_sub_category: csvData.product_sub_category[index],
            product_ItemGroupID: csvData.product_ItemGroupID[index],
            product_group_num: csvData.product_group_num[index],
            product_total_rating: csvData.product_total_rating[index],
          };
        });

        // Write the CSV
        const writer = csvWriter({
          path: 'product_info.csv',
          header: Object.keys(records[0]).map(key => ({ id: key, title: key })),
        });

        await writer.writeRecords(records);
        console.log('Data saved to product_info.csv');
        await browser.close();
      });
  } catch (error) {
    console.error('Error:', error);
  }
})();
