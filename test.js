const express = require("express");
const app = express();

const quotes = [
  { text: "An eye for an eye.", title: "Mahatma Gandhi" },
  { text: "When in doubt, tell the truth.", title: "Mark Twain" },
  { text: "You are who you choose to be.", title: "Mark Twain" },
];

// Helper to get a random quote
function getRandomQuote() {
  const index = Math.floor(Math.random() * quotes.length);
  return quotes[index];
}

// Route
app.get("/quotes/random", function (req, res) {
  const randomQuote = getRandomQuote();
  res.json(randomQuote);
});

// Start server
app.listen(8003, function () {
  console.log("Express app running at http://127.0.0.1:8003/");
});
