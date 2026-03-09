const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Serve static files from the current directory
app.use(express.static(path.join(__dirname)));

// API endpoint for brand generation (placeholder)
app.get('/generate', (req, res) => {
  const keyword = req.query.keyword;
  // Simple mock response - in real app, integrate with AI API
  const brands = [
    `${keyword}Hub`,
    `${keyword}Pro`,
    `${keyword}AI`,
    `${keyword}Tech`,
    `${keyword}Solutions`
  ];
  res.json({ brands });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});