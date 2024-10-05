var express = require('express');
var router = express.Router();


/* GET home page. */


const http = require('https');

const options = {
	method: 'GET',
	hostname: 'asos2.p.rapidapi.com',
	port: null,
	path: `/products/v2/list?store=US&offset=0&categoryId=4209&sort=freshness&q=${queryString}&limit=48&lang=en-US`,
	headers: {
		'x-rapidapi-key': `${process.env.RapidApi_KEY}`,
		'x-rapidapi-host': `${process.env.Rapid_HOST}`
	}
};
router.get('/Products', async (req,res)=> {
  const queryString = req.query;

 

http.request(options, function (res) {
	const chunks = [];

	res.on('data', function (chunk) {
		chunks.push(chunk);
	});

	res.on('end', function () {
		const body = Buffer.concat(chunks);
		console.log(body.toString());
	});
});

req.end();

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
