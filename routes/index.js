var express = require('express');
var router = express.Router();


/* GET home page. */





router.get('/Products', async (req,res) => {
  const query = req.query;
  try {
    if (!query.trim()) {
      res.status(400).json({errror:'A query is needed to proceed with the request'})
    }

    const request = await fetch(`https://api.barcodelookup.com/v3/products?title=${params}&manufacturer=${params}&key=${process.env.API_KEY}`);
    const data = await response.json({results: request.products})
    const results = data.map(item => ({
      title: item.title,
      brand:item.brand,
      description:item.description,
      image:item.image,
    }))

    res.json({results});
    console.log('result object filtered', results)

  } catch (error) {
    console.error('We experienced an issue with /Products endpoint',error)
    res.status(500).json({error:'Something went wrong'})
  }
})

module.exports = router;
