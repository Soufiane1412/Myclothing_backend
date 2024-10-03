var express = require('express');
var router = express.Router();


/* GET home page. */



router.get('/Products', async (req,res) => {
  console.log('querying')

  const queryParams = req.query;
    if (Object.keys(queryParams).length===0) {
      res.status(400).json({errror:'A query is needed to proceed with the request'})
    }
  try {

    const queryString = Object.entries(queryParams)
    .map(([key, value])=> `${key}=${value}`)
    .join('&');

    console.log('constructed query string', queryString)

    const response = await fetch(`https://api.barcodelookup.com/v3/products?${queryString}&key=${process.env.API_KEY}`);
    const data = await response.json()

    console.log('API response', response.status)

    const results = data.map(item => ({
      title: item.title,
      brand:item.brand,
      description:item.description,
      image:item.image,
    }))

    res.json({results});

  } catch (error) {
    console.error('We experienced an issue with /Products endpoint',error)
    res.status(500).json({error:'Something went wrong'})
  }
})

module.exports = router;