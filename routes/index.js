var express = require('express');
var router = express.Router();


/* GET home page. */


router.get('/Products', async (req,res)=> {

  
  const queryString = req.query.q;
  const url = `https://asos2.p.rapidapi.com/products/v2/list?store=US&offset=0&categoryId=4209&sort=freshness&q=${encodeURIComponent(queryString)}&limit=48&lang=en-US`
  const options = {
    method: 'GET',
    headers: {
      'x-rapidapi-key': `${process.env.RapidApi_KEY}`,
      'x-rapidapi-host': `${process.env.Rapid_HOST}`
    }
  }

  try{
    const response = await fetch(url, options);
    console.log('response status:', response.status);
    const rawResponse = await response.text();
    console.log('raw response:', rawResponse);

    if (!response.ok) {
      return res.status(500).json({error: 'error whilst fetching the data', status: response.status})
    }
    const results = await response.json();
    console.log('Response Json():', results)
    
    if (!results.products || results.products.length===0) {
      res.status(404).json({error: 'error no products were found, try again'})
    }
    const filteredResponse = results.products.map(item=> ({
      name:item.name,
      price:item.price.current.text,
      colour:item.colour,
      brand:item.brandName,
      image:item.imageUrl,
    }))
    
    console.log('Filtered Response',filteredResponse)
  } catch (error) {
    console.error('Error', error);
    res.status(500).json({error: 'server error', details: error.message})
  }
})






// router.get('/Products', async (req,res) => {
//   console.log('querying')

//   const queryParams = req.query;
//     if (Object.keys(queryParams).length===0) {
//       res.status(400).json({errror:'A query is needed to proceed with the request'})
//     }
//   try {

//     const queryString = Object.entries(queryParams)
//     .map(([key, value])=> `${key}=${value}`)
//     .join('&');

//     console.log('constructed query string', queryString)

//     const response = await fetch(`https://api.barcodelookup.com/v3/products?${queryString}&key=${process.env.API_KEY}`);

//     if (!response.ok) {
//       console.log('API response not OK:', response.status)
//       return res.status(500).json({error: 'error when fetching data'})
//     }
//     const data = res.json();
//     console.log('API raw data', response)

//     if (!data.products || data.products.length===0) {
//     return res.status(404).json({error: 'No products found'})
//     }

//     const result = data.products.map(item => ({
//       title:item.title,
//       brand:item.brand,
//       description:item.description,
//       image:item.image,
//     }));

//     return result

//   } catch (error) {
//     console.error('We experienced an issue with /Products endpoint',error)
//     res.status(500).json({error:'Something went wrong'})
//   }
// })

module.exports = router;
